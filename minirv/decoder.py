"""Decodificador (Semana 01): reconhece ADD e ADDI. Será generalizado na Semana 07."""

from minirv.word32 import MASK32


def decode(word):
    if isinstance(word, bool) or not isinstance(word, int) or not 0 <= word <= MASK32:
        raise ValueError(f"palavra inválida (esperado inteiro de 32 bits): {word!r}")
    opcode = word & 0x7F
    rd = (word >> 7) & 0x1F
    funct3 = (word >> 12) & 0x7
    rs1 = (word >> 15) & 0x1F
    rs2 = (word >> 20) & 0x1F
    funct7 = (word >> 25) & 0x7F
    if opcode == 0b0110011 and funct3 == 0 and funct7 == 0:
        return {"mnemonic": "ADD", "format": "R", "rd": rd, "rs1": rs1, "rs2": rs2}
    if opcode == 0b0010011 and funct3 == 0:
        imm = word >> 20
        if imm & 0x800:
            imm -= 0x1000
        return {"mnemonic": "ADDI", "format": "I", "rd": rd, "rs1": rs1, "imm": imm}
    raise ValueError(f"instrução não suportada: 0x{word:08X}")


def format_assembly(d):
    m = d["mnemonic"]
    if m == "ADD":
        return f"ADD x{d['rd']}, x{d['rs1']}, x{d['rs2']}"
    if m == "ADDI":
        return f"ADDI x{d['rd']}, x{d['rs1']}, {d['imm']}"
    raise ValueError(f"mnemônico não suportado: {m!r}")
