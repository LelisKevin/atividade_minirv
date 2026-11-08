"""Multiplexador 2:1."""


def mux2(sel, entrada0, entrada1):
    """sel = 0 encaminha entrada0; sel = 1 encaminha entrada1. O seletor não altera os dados."""
    if type(sel) is not int or sel not in (0, 1):
        raise ValueError(f"sel inválido: {sel!r} (esperado 0 ou 1)")
    if sel == 0:
        return entrada0
    return entrada1
