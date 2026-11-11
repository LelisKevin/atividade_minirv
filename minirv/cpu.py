"""CPU RV32I reduzida: executa instruções suportadas uma a uma e gera trace."""
import argparse
import sys
import threading

from minirv.alu import execute
from minirv.data_memory import DataMemory
from minirv.decoder import decode, format_assembly
from minirv.instruction_memory import InstructionMemory
from minirv.pc import ProgramCounter
from minirv.registers import RegisterFile
from minirv.trace import Trace, hex32
from minirv.word32 import MASK32, normalizar32


def load_hex(path):
    """Lê um arquivo .hex: uma palavra de 32 bits por linha; '#' inicia comentário."""
    words = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            token = line.split("#", 1)[0].strip()
            if not token:
                continue
            try:
                word = int(token, 16)
            except ValueError:
                raise ValueError(f"{path}:{n}: hexadecimal inválido: {token!r}") from None
            if not 0 <= word <= MASK32:
                raise ValueError(f"{path}:{n}: palavra fora de 32 bits: {token!r}")
            words.append(word)
    return words


class CPU:
    def __init__(self, program, memory=None, trace_enabled=True):
        self.imem = InstructionMemory(program)
        self.memory = memory if memory is not None else DataMemory()
        self.regs = RegisterFile()
        self._pc = ProgramCounter()
        self.trace = Trace()
        self.trace_enabled = trace_enabled
        self.instruction_count = 0
        self.halted = False
        self._execution_lock = threading.Lock()

    @property
    def pc(self):
        return self._pc.value()

    def reset(self):
        """Reinicia PC, registradores, trace e estado de parada; preserva as memórias."""
        with self._execution_lock:
            self._pc.reset()
            self.regs = RegisterFile()
            self.trace = Trace()
            self.instruction_count = 0
            self.halted = False

    def write_memory_word(self, address, value):
        """Escreve na memória de dados e retorna o contador de instruções no mesmo ponto de sincronização."""
        with self._execution_lock:
            self.memory.write_word(address, value)
            return self.instruction_count

    def step(self):
        """Executa uma instrução. Retorna o registro de trace, ou None se o programa terminou."""
        with self._execution_lock:
            return self._step()

    def _step(self):
        if self.halted:
            return None
        if self.pc >= self.imem.size_bytes:
            self.halted = True  # fim do programa: PC saiu da memória de instruções
            return None
        pc_before = self.pc
        word = self.imem.read_word(pc_before)
        d = decode(word)
        mnemonic = d["mnemonic"]
        supported = ("ADD", "ADDI", "LUI", "LW", "SW", "BEQ", "JAL")
        if mnemonic not in supported:
            raise ValueError(f"instrução decodificada, mas ainda não executada pela CPU: {d['mnemonic']} "
                             f"(pc {hex32(pc_before)}); instrução fora do subconjunto executável atual")

        written = {}
        read = {}
        next_pc = normalizar32(pc_before + 4)

        if mnemonic == "ADD":
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"]), f"x{d['rs2']}": self.regs.read(d["rs2"])}
            result = execute("ADD", self.regs.read(d["rs1"]), self.regs.read(d["rs2"]))
            self.regs.write(d["rd"], result)
        elif mnemonic == "ADDI":
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"])}
            result = execute("ADD", self.regs.read(d["rs1"]), normalizar32(d["imm"]))
            self.regs.write(d["rd"], result)
        elif mnemonic == "LUI":
            result = normalizar32(d["imm"] << 12)
            self.regs.write(d["rd"], result)
        elif mnemonic == "LW":
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"])}
            address = normalizar32(read[f"x{d['rs1']}"] + d["imm"])
            result = self.memory.read_word(address)
            self.regs.write(d["rd"], result)
        elif mnemonic == "SW":
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"]), f"x{d['rs2']}": self.regs.read(d["rs2"])}
            address = normalizar32(read[f"x{d['rs1']}"] + d["imm"])
            self.memory.write_word(address, read[f"x{d['rs2']}"])
        elif mnemonic == "BEQ":
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"]), f"x{d['rs2']}": self.regs.read(d["rs2"])}
            if read[f"x{d['rs1']}"] == read[f"x{d['rs2']}"]:
                next_pc = normalizar32(pc_before + d["imm"])
        elif mnemonic == "JAL":
            self.regs.write(d["rd"], next_pc)
            next_pc = normalizar32(pc_before + d["imm"])

        if "rd" in d and d["rd"] != 0 and mnemonic in ("ADD", "ADDI", "LUI", "LW", "JAL"):
            written[f"x{d['rd']}"] = self.regs.read(d["rd"])
        if mnemonic == "SW":
            written[f"mem[{address}]"] = self.memory.read_word(address)

        self._pc.jump(next_pc)
        self.instruction_count += 1
        record = {
            "pc": hex32(pc_before),
            "instruction": format_assembly(d),
            "registers_read": read,
            "registers_written": written,
            "next_pc": hex32(self.pc),
        }
        if self.trace_enabled:
            self.trace.add(record)
        return record

    def run(self, max_steps=100_000):
        steps = 0
        while self.step() is not None:
            steps += 1
            if steps >= max_steps:
                raise RuntimeError(f"limite de {max_steps} passos excedido")
        return steps


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m minirv.cpu", description="Executa um programa .hex no MiniRV")
    p.add_argument("program", help="arquivo .hex (uma palavra de 32 bits por linha)")
    p.add_argument("-o", "--output", help="salva o trace JSON neste arquivo")
    p.add_argument("--step", action="store_true", help="modo passo a passo (Enter avança)")
    p.add_argument("--max-steps", type=int, default=100_000)
    args = p.parse_args(argv)

    cpu = CPU(load_hex(args.program))
    if args.step:
        while True:
            rec = cpu.step()
            if rec is None:
                break
            print(f"{rec['pc']}: {rec['instruction']:<20} escreve {rec['registers_written']} -> PC {rec['next_pc']}")
            input("[Enter] próxima instrução... ")
    else:
        cpu.run(args.max_steps)

    if args.output:
        cpu.trace.save(args.output)
    elif not args.step:
        print(cpu.trace.to_json())
    nonzero = {k: v for k, v in cpu.regs.dump().items() if v}
    print(f"# registradores não nulos: {nonzero} | PC final: {hex32(cpu.pc)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
