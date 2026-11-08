"""Portas lógicas AND, OR, NOT e XOR. Aceitam somente os inteiros 0 e 1 (bool e float são rejeitados)."""


def bit(x):
    # type(x) is int rejeita True/False e 1.0, que o Python trataria como 1/0 em `x in (0, 1)`.
    if type(x) is not int or x not in (0, 1):
        raise ValueError(f"Entrada deve ser 0 ou 1: {x!r}")
    return x


def NOT(a):
    """NOT inverte o bit: 0 vira 1 e 1 vira 0."""
    a = bit(a)
    return 1 - a


def AND(a, b):
    """AND vale 1 somente quando as duas entradas valem 1."""
    a, b = bit(a), bit(b)
    return 1 if a == 1 and b == 1 else 0


def OR(a, b):
    """OR vale 1 quando pelo menos uma entrada vale 1."""
    a, b = bit(a), bit(b)
    return 1 if a == 1 or b == 1 else 0


def XOR(a, b):
    """XOR vale 1 quando as entradas são diferentes."""
    a, b = bit(a), bit(b)
    return 1 if a != b else 0


def xor_sop(a, b):
    """XOR montado por Soma de Produtos: S = ¬A·B + A·¬B (evidência do método estudado)."""
    return OR(AND(NOT(a), b), AND(a, NOT(b)))
