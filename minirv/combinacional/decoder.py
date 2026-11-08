"""Decodificador 2→4: AB formam um número de 0 a 3 e exatamente uma saída vale 1."""


def decoder2to4(a, b):
    if type(a) is not int or type(b) is not int or a not in (0, 1) or b not in (0, 1):
        raise ValueError(f"Entradas do decoder devem ser 0 ou 1: a={a!r}, b={b!r}")
    indice = (a * 2) + b
    saidas = [0, 0, 0, 0]
    saidas[indice] = 1
    return tuple(saidas)
