"""Especificação do subconjunto RV32I v1, lida de docs/isa/rv32i-subset-v1.md (fonte única de verdade).

encoder.py e decoder.py usam SPEC; não há tabela de codificação duplicada no código.
"""
import re
from dataclasses import dataclass
from pathlib import Path

CONTRATO = Path(__file__).resolve().parent.parent / "docs" / "isa" / "rv32i-subset-v1.md"
INICIO, FIM = "<!-- ISA-TABLE:BEGIN -->", "<!-- ISA-TABLE:END -->"
OBRIGATORIAS = ("ADD", "SUB", "AND", "OR", "XOR", "SLT", "SLL", "SRL", "ADDI", "ANDI", "ORI", "LW", "JALR", "SW",
                "BEQ", "BNE", "BLT", "JAL", "LUI")
FORMATOS = ("R", "I", "S", "B", "U", "J")
CAMPOS_VALIDOS = ("rd", "rs1", "rs2", "imm")
REGISTRADORES = range(32)


class ISAError(ValueError):
    """Base dos erros do contrato da ISA."""


class InvalidRegisterError(ISAError):
    pass


class ImmediateRangeError(ISAError):
    pass


class UnsupportedInstructionError(ISAError):
    pass


class FieldMismatchError(ISAError):
    pass


class InvalidWordError(ISAError):
    pass


@dataclass(frozen=True)
class InstructionSpec:
    mnemonic: str
    format: str
    syntax: str
    opcode: int
    funct3: "int | None"
    funct7: "int | None"
    fields: tuple
    imm_min: "int | None"
    imm_max: "int | None"
    imm_align: int


def _binario(texto, largura, ctx):
    if texto == "—":
        return None
    if not re.fullmatch(r"[01]{%d}" % largura, texto):
        raise ValueError(f"contrato: {ctx}: esperado {largura} bits binários, obtido {texto!r}")
    return int(texto, 2)


def _linha(celulas):
    mnem, fmt, sintaxe, opc, f3, f7, campos, faixa, _sem, _erro = celulas
    if fmt not in FORMATOS:
        raise ValueError(f"contrato: {mnem}: formato inválido {fmt!r}")
    fields = tuple(c.strip() for c in campos.split(","))
    if any(c not in CAMPOS_VALIDOS for c in fields):
        raise ValueError(f"contrato: {mnem}: campo desconhecido em {campos!r}")
    imm_min = imm_max = None
    alinhamento = 1
    m = re.search(r"imm:\s*(-?\d+)\.\.(-?\d+)", faixa)
    if "imm" in fields:
        if not m:
            raise ValueError(f"contrato: {mnem}: faixa do imediato ausente em {faixa!r}")
        imm_min, imm_max = int(m.group(1)), int(m.group(2))
        a = re.search(r"múltiplo de (\d+)", faixa)
        alinhamento = int(a.group(1)) if a else 1
    return InstructionSpec(mnem, fmt, sintaxe, _binario(opc, 7, mnem), _binario(f3, 3, mnem),
                           _binario(f7, 7, mnem), fields, imm_min, imm_max, alinhamento)


def load_spec(path=CONTRATO):
    texto = Path(path).read_text(encoding="utf-8")
    if INICIO not in texto or FIM not in texto:
        raise ValueError(f"contrato: marcadores da tabela não encontrados em {path}")
    bloco = texto.split(INICIO, 1)[1].split(FIM, 1)[0]
    linhas = [l for l in bloco.splitlines() if l.startswith("|")][2:]  # descarta cabeçalho e separador
    spec = {}
    for l in linhas:
        celulas = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(celulas) != 10:
            raise ValueError(f"contrato: linha com {len(celulas)} colunas (esperado 10): {l[:50]}")
        item = _linha(celulas)
        if item.mnemonic in spec:
            raise ValueError(f"contrato: mnemônico duplicado: {item.mnemonic}")
        spec[item.mnemonic] = item
    faltando = [m for m in OBRIGATORIAS if m not in spec]
    extras = [m for m in spec if m not in OBRIGATORIAS]
    if faltando or extras:
        raise ValueError(f"contrato: instruções faltando {faltando}, a mais {extras}")
    return spec


SPEC = load_spec()


def verificar_registrador(valor, campo, mnemonico):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor not in REGISTRADORES:
        raise InvalidRegisterError(
            f"registrador inválido: {_reg(valor)} no campo {campo} de {mnemonico} (válidos: x0 a x31)")


def _reg(valor):
    return f"x{valor}" if isinstance(valor, int) and not isinstance(valor, bool) else repr(valor)


def verificar_imediato(spec, imm):
    m = spec.mnemonic
    if isinstance(imm, bool) or not isinstance(imm, int):
        raise ImmediateRangeError(f"imediato inválido em {m}: {imm!r} (esperado inteiro)")
    if not spec.imm_min <= imm <= spec.imm_max:
        raise ImmediateRangeError(
            f"imediato fora da faixa: {imm} em {m} (aceito: {spec.imm_min} a {spec.imm_max})")
    if imm % spec.imm_align:
        raise ImmediateRangeError(f"imediato desalinhado: {imm} em {m} (exige múltiplo de {spec.imm_align})")
