"""encode: instrução estruturada -> palavra de 32 bits, conforme docs/isa/rv32i-subset-v1.md."""
from minirv.isa import (SPEC, FieldMismatchError, UnsupportedInstructionError, verificar_imediato,
                        verificar_registrador)

_CONTROLE = {"mnemonic", "format"}


def encode(instr):
    """encode({"mnemonic": "ADD", "rd": 3, "rs1": 1, "rs2": 2}) -> 0x002081B3"""
    if not isinstance(instr, dict) or not isinstance(instr.get("mnemonic"), str):
        raise FieldMismatchError(f"campo ausente: instrução deve ser dict com 'mnemonic' ({instr!r})")
    m = instr["mnemonic"]
    if m not in SPEC:
        raise UnsupportedInstructionError(f"instrução não suportada: {m}")
    spec = SPEC[m]
    if "format" in instr and instr["format"] != spec.format:
        raise FieldMismatchError(
            f"campo incompatível: format {instr['format']!r} em {m} (formato correto: {spec.format})")
    dados = {k: v for k, v in instr.items() if k not in _CONTROLE}
    for campo in dados:
        if campo not in spec.fields:
            raise FieldMismatchError(f"campo incompatível: {m} não possui {campo}")
    for campo in spec.fields:
        if campo not in dados:
            raise FieldMismatchError(f"campo ausente: {m} exige {campo}")
    for campo in ("rd", "rs1", "rs2"):
        if campo in dados:
            verificar_registrador(dados[campo], campo, m)
    if "imm" in dados:
        verificar_imediato(spec, dados["imm"])

    rd, rs1, rs2, imm = (dados.get(c, 0) for c in ("rd", "rs1", "rs2", "imm"))
    f3 = spec.funct3 or 0
    f7 = spec.funct7 or 0
    op = spec.opcode
    f = spec.format
    if f == "R":
        return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op
    if f == "I":
        return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op
    if f == "S":
        return (((imm >> 5) & 0x7F) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | ((imm & 0x1F) << 7) | op
    if f == "B":
        return (((imm >> 12) & 1) << 31) | (((imm >> 5) & 0x3F) << 25) | (rs2 << 20) | (rs1 << 15) \
            | (f3 << 12) | (((imm >> 1) & 0xF) << 8) | (((imm >> 11) & 1) << 7) | op
    if f == "U":
        return (imm << 12) | (rd << 7) | op
    # J
    return (((imm >> 20) & 1) << 31) | (((imm >> 1) & 0x3FF) << 21) | (((imm >> 11) & 1) << 20) \
        | (((imm >> 12) & 0xFF) << 12) | (rd << 7) | op
