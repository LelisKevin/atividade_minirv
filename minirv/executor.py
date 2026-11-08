"""Executor do ciclo de instrução (Semana 06).

Decomposição DIDÁTICA em cinco estados (não é um pipeline): FETCH, DECODE, EXECUTE, MEMORY, WRITEBACK.
Cada estado emite um evento de rastro {seq, pc, word, stage, signals, operands, change}.

As três palavras abaixo são IDENTIFICADORES DIDÁTICOS CONTROLADOS, NÃO são codificações RV32I reais:
    0x01000001  CADD    x3 ← x1 + x2
    0x02000002  CSTORE  memória[0] ← x3
    0x03000003  CLOAD   x4 ← memória[0]
(As codificações RV32I reais são do contrato da Semana 07, em minirv/isa.py.)
"""
import argparse
import sys

from minirv.alu import execute
from minirv.combinacional.control import OPCODE_LOAD, OPCODE_R, OPCODE_STORE, decode_control
from minirv.combinacional.mux import mux2
from minirv.data_memory import DataMemory
from minirv.instruction_memory import InstructionMemory
from minirv.pc import ProgramCounter
from minirv.registers import RegisterFile
from minirv.trace import Trace, hex32

ESTADOS = ("FETCH", "DECODE", "EXECUTE", "MEMORY", "WRITEBACK")

# word -> (nome, classe de controle, rd, rs1, rs2, imediato)
INSTRUCOES_CONTROLADAS = {
    0x01000001: {"nome": "CADD", "opcode": OPCODE_R, "rd": 3, "rs1": 1, "rs2": 2, "imm": 0},
    0x02000002: {"nome": "CSTORE", "opcode": OPCODE_STORE, "rd": None, "rs1": 0, "rs2": 3, "imm": 0},
    0x03000003: {"nome": "CLOAD", "opcode": OPCODE_LOAD, "rd": 4, "rs1": 0, "rs2": None, "imm": 0},
}


class Executor:
    def __init__(self, imem, dmem, regs, pc, trace=None):
        self.imem, self.dmem, self.regs, self.pc = imem, dmem, regs, pc
        self.trace = trace if trace is not None else Trace()
        self._seq = 0
        self._indice_estado = 0
        self._ctx = {}

    @property
    def current_stage(self):
        """Próximo estado a executar."""
        return ESTADOS[self._indice_estado]

    @property
    def finished(self):
        """Verdadeiro quando o PC saiu da memória de instruções e nenhuma instrução está em curso."""
        return self._indice_estado == 0 and self.pc.value() >= self.imem.size_bytes

    def _emit(self, stage, signals=None, operands=None, change=None):
        self._seq += 1
        evento = {
            "seq": self._seq,
            "pc": hex32(self._ctx["pc"]),
            "word": hex32(self._ctx["word"]),
            "stage": stage,
            "signals": signals or {},
            "operands": operands or {},
            "change": change or {},
        }
        self.trace.add(evento)
        return evento

    # ---- os cinco estados ----
    def _fetch(self):
        self._ctx = {"pc": self.pc.value()}
        self._ctx["word"] = self.imem.read_word(self._ctx["pc"])
        return self._emit("FETCH", {"IMemRead": 1})

    def _decode(self):
        word = self._ctx["word"]
        if word not in INSTRUCOES_CONTROLADAS:
            raise ValueError(f"instrução controlada desconhecida: {hex32(word)} (pc {hex32(self._ctx['pc'])})")
        ins = INSTRUCOES_CONTROLADAS[word]
        sinais = decode_control(ins["opcode"])
        self._ctx["ins"], self._ctx["sinais"] = ins, sinais
        lidos = {}
        if ins["rs1"] is not None:
            lidos[f"x{ins['rs1']}"] = self.regs.read(ins["rs1"])
        if ins["rs2"] is not None:
            lidos[f"x{ins['rs2']}"] = self.regs.read(ins["rs2"])
        self._ctx["lidos"] = lidos
        self._ctx["a"] = self.regs.read(ins["rs1"])
        self._ctx["reg_b"] = self.regs.read(ins["rs2"]) if ins["rs2"] is not None else 0
        self._ctx["valor_store"] = self.regs.read(ins["rs2"]) if sinais["MemWrite"] else None
        sig = {"op": ins["nome"], **{k: v for k, v in sinais.items()}}
        return self._emit("DECODE", sig, dict(lidos))

    def _execute(self):
        ins, sinais = self._ctx["ins"], self._ctx["sinais"]
        # MUX ALUSrc: 0 = registrador (rs2), 1 = imediato
        b = mux2(sinais["ALUSrc"], self._ctx["reg_b"], ins["imm"])
        resultado = execute("ADD", self._ctx["a"], b)  # CADD: soma; CLOAD/CSTORE: endereço efetivo
        self._ctx["resultado"] = resultado
        return self._emit("EXECUTE", {"ALUOp": "ADD", "ALUSrc": sinais["ALUSrc"]},
                          {"a": self._ctx["a"], "b": b, "alu_result": resultado})

    def _memory(self):
        sinais = self._ctx["sinais"]
        sig = {"MemRead": sinais["MemRead"], "MemWrite": sinais["MemWrite"]}
        endereco = self._ctx["resultado"]
        if sinais["MemWrite"]:
            self.dmem.write_word(endereco, self._ctx["valor_store"])
            return self._emit("MEMORY", sig, {"address": endereco, "value": self._ctx["valor_store"]},
                              {f"mem[{endereco}]": self.dmem.read_word(endereco)})
        if sinais["MemRead"]:
            self._ctx["dado_lido"] = self.dmem.read_word(endereco)
            return self._emit("MEMORY", sig, {"address": endereco, "value": self._ctx["dado_lido"]})
        return self._emit("MEMORY", sig)

    def _writeback(self):
        ins, sinais = self._ctx["ins"], self._ctx["sinais"]
        mudanca = {}
        if sinais["RegWrite"]:
            valor = self._ctx["dado_lido"] if sinais["MemRead"] else self._ctx["resultado"]
            self.regs.write(ins["rd"], valor, enable=True)
            mudanca[f"x{ins['rd']}"] = self.regs.read(ins["rd"])
        self.pc.advance()
        mudanca["pc_next"] = hex32(self.pc.value())
        return self._emit("WRITEBACK", {"RegWrite": sinais["RegWrite"]}, dict(self._ctx["lidos"]), mudanca)

    def step_stage(self):
        """Executa o estado atual e avança para o próximo. Retorna o evento de rastro (None se terminou)."""
        if self.finished:
            return None
        evento = (self._fetch, self._decode, self._execute, self._memory, self._writeback)[self._indice_estado]()
        self._indice_estado = (self._indice_estado + 1) % len(ESTADOS)
        return evento

    def step_instruction(self):
        """Executa os cinco estados de uma instrução. Retorna a lista de eventos (vazia se terminou)."""
        eventos = []
        while True:
            ev = self.step_stage()
            if ev is None:
                return eventos
            eventos.append(ev)
            if self._indice_estado == 0:
                return eventos

    def run(self):
        n = 0
        while self.step_instruction():
            n += 1
        return n


def micro_sequencia():
    """Cria o executor com o estado inicial obrigatório: x1=5, x2=7, x3=0, x4=0, memória[0]=0, PC=0."""
    regs = RegisterFile()
    regs.write(1, 5)
    regs.write(2, 7)
    return Executor(InstructionMemory(list(INSTRUCOES_CONTROLADAS)), DataMemory(), regs, ProgramCounter())


def estado_final(ex):
    return {"x3": ex.regs.read(3), "memória[0]": ex.dmem.read_word(0), "x4": ex.regs.read(4),
            "PC final": hex32(ex.pc.value())}


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m minirv.executor",
                                description="Executa a microssequência controlada da Semana 06")
    p.add_argument("--trace", help="salva o rastro arquitetural JSON neste caminho")
    args = p.parse_args(argv)
    ex = micro_sequencia()
    ex.run()
    if args.trace:
        ex.trace.save(args.trace)
    print(f"{len(ex.trace)} eventos | estado final: {estado_final(ex)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
