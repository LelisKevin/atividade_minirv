"""CPU mínima (Semana 01): executa uma instrução por vez (ADD/ADDI) e gera trace."""
import argparse
import sys

from minirv.alu import execute
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
    def __init__(self, program):
        self.imem = InstructionMemory(program)
        self.regs = RegisterFile()
        self._pc = ProgramCounter()
        self.trace = Trace()
        self.halted = False

    @property
    def pc(self):
        return self._pc.value()

    def step(self):
        """Executa uma instrução. Retorna o registro de trace, ou None se o programa terminou."""
        if self.halted:
            return None
        if self.pc >= self.imem.size_bytes:
            self.halted = True  # fim do programa: PC saiu da memória de instruções
            return None
        word = self.imem.read_word(self.pc)
        d = decode(word)
        if d["mnemonic"] not in ("ADD", "ADDI"):
            raise ValueError(f"instrução decodificada, mas ainda não executada pela CPU: {d['mnemonic']} "
                             f"(pc {hex32(self.pc)}); o caminho de dados completo é de outra etapa")
        written = {}
        if d["mnemonic"] == "ADD":
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"]), f"x{d['rs2']}": self.regs.read(d["rs2"])}
            result = execute("ADD", self.regs.read(d["rs1"]), self.regs.read(d["rs2"]))
        else:  # ADDI
            read = {f"x{d['rs1']}": self.regs.read(d["rs1"])}
            result = execute("ADD", self.regs.read(d["rs1"]), normalizar32(d["imm"]))
        self.regs.write(d["rd"], result)
        if d["rd"] != 0:
            written[f"x{d['rd']}"] = self.regs.read(d["rd"])
        pc_before = self.pc
        self._pc.advance()
        record = {
            "pc": hex32(pc_before),
            "instruction": format_assembly(d),
            "registers_read": read,
            "registers_written": written,
            "next_pc": hex32(self.pc),
        }
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
