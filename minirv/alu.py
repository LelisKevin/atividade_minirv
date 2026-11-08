"""ULA (Semana 01): apenas ADD. Será estendida na Semana 05."""

MASK32 = 0xFFFFFFFF


def execute(op, a, b):
    if op == "ADD":
        return (a + b) & MASK32
    raise ValueError(f"operação de ULA desconhecida: {op!r}")
