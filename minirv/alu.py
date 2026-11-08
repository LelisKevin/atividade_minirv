"""ULA (Semana 01): apenas ADD. Será estendida na Semana 05."""
from minirv.word32 import normalizar32


def execute(op, a, b):
    if op == "ADD":
        return normalizar32(normalizar32(a) + normalizar32(b))
    raise ValueError(f"operação de ULA desconhecida: {op!r}")
