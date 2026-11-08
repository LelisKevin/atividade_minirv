"""ULA de 32 bits (Semanas 01 e 05).

Combinacional: mesmas entradas e mesma operação produzem sempre a mesma saída; não altera estado global.
Operações: ADD, SUB, AND, OR, XOR, SLT (com sinal), SLL e SRL (lógico).
Deslocamentos usam apenas os 5 bits menos significativos de b (0..31), como no RV32I.
"""
from minirv.word32 import normalizar32, para_signed32

OPERACOES = ("ADD", "SUB", "AND", "OR", "XOR", "SLT", "SLL", "SRL")


def execute(op, a, b):
    a = normalizar32(a)
    b = normalizar32(b)
    if op == "ADD":
        return normalizar32(a + b)
    if op == "SUB":
        return normalizar32(a - b)
    if op == "AND":
        return a & b
    if op == "OR":
        return a | b
    if op == "XOR":
        return a ^ b
    if op == "SLT":
        return 1 if para_signed32(a) < para_signed32(b) else 0
    if op == "SLL":
        return normalizar32(a << (b & 0x1F))
    if op == "SRL":
        return a >> (b & 0x1F)
    raise ValueError(f"operação de ULA desconhecida: {op!r}")
