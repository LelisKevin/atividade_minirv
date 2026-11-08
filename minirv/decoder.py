"""decode: palavra de 32 bits -> instrução estruturada, conforme docs/isa/rv32i-subset-v1.md.

Só devolve os campos que pertencem ao formato (SW não tem rd; LUI não tem rs1/rs2).
format_assembly() escreve a sintaxe canônica a partir da coluna "Sintaxe" do contrato.
"""
import re

from minirv.isa import SPEC, InvalidWordError, UnsupportedInstructionError, verificar_imediato
from minirv.word32 import MASK32, estender_sinal, para_signed32

_POR_OPCODE = {}
for _s in SPEC.values():
    _POR_OPCODE.setdefault(_s.opcode, []).append(_s)


def _imediato(spec, w):
    f = spec.format
    if f == "I":
        return para_signed32(estender_sinal(w >> 20, 12))
    if f == "S":
        return para_signed32(estender_sinal(((w >> 25) << 5) | ((w >> 7) & 0x1F), 12))
    if f == "B":
        bruto = ((w >> 31) << 12) | (((w >> 7) & 1) << 11) | (((w >> 25) & 0x3F) << 5) | (((w >> 8) & 0xF) << 1)
        return para_signed32(estender_sinal(bruto, 13))
    if f == "U":
        return w >> 12
    bruto = ((w >> 31) << 20) | (((w >> 12) & 0xFF) << 12) | (((w >> 20) & 1) << 11) | (((w >> 21) & 0x3FF) << 1)
    return para_signed32(estender_sinal(bruto, 21))  # J


def decode(word):
    if isinstance(word, bool) or not isinstance(word, int) or not 0 <= word <= MASK32:
        raise InvalidWordError(f"palavra inválida (esperado inteiro de 32 bits): {word!r}")
    opcode = word & 0x7F
    f3 = (word >> 12) & 0x7
    f7 = (word >> 25) & 0x7F
    spec = next((s for s in _POR_OPCODE.get(opcode, [])
                 if (s.funct3 is None or s.funct3 == f3) and (s.funct7 is None or s.funct7 == f7)), None)
    if spec is None:
        raise UnsupportedInstructionError(
            f"instrução não suportada: 0x{word:08X} (opcode={opcode:07b}, funct3={f3:03b}, funct7={f7:07b})")
    saida = {"mnemonic": spec.mnemonic, "format": spec.format}
    if "rd" in spec.fields:
        saida["rd"] = (word >> 7) & 0x1F
    if "rs1" in spec.fields:
        saida["rs1"] = (word >> 15) & 0x1F
    if "rs2" in spec.fields:
        saida["rs2"] = (word >> 20) & 0x1F
    if "imm" in spec.fields:
        saida["imm"] = _imediato(spec, word)
        verificar_imediato(spec, saida["imm"])  # ex.: branch com deslocamento não múltiplo de 4
    return saida


def format_assembly(d):
    spec = SPEC.get(d.get("mnemonic"))
    if spec is None:
        raise UnsupportedInstructionError(f"instrução não suportada: {d.get('mnemonic')}")

    def troca(m):
        campo = m.group(1)
        if campo == "imm":
            return f"0x{d['imm']:X}" if spec.mnemonic == "LUI" else str(d["imm"])
        return f"x{d[campo]}"

    return re.sub(r"\b(rd|rs1|rs2|imm)\b", troca, spec.syntax)
