import itertools

import pytest

from minirv.combinacional.decoder import decoder2to4


@pytest.mark.parametrize("a,b,esperado", [
    (0, 0, (1, 0, 0, 0)),
    (0, 1, (0, 1, 0, 0)),
    (1, 0, (0, 0, 1, 0)),
    (1, 1, (0, 0, 0, 1)),
])
def test_tabela_do_decoder(a, b, esperado):
    assert decoder2to4(a, b) == esperado


def test_uma_e_somente_uma_saida_ativa():
    for a, b in itertools.product((0, 1), repeat=2):
        saidas = decoder2to4(a, b)
        assert len(saidas) == 4 and sum(saidas) == 1 and saidas[a * 2 + b] == 1


@pytest.mark.parametrize("a,b", [(2, 0), (0, 2), (-1, 1), (None, 0), (0, "1"), (True, 0), (1.0, 1)])
def test_entrada_invalida(a, b):
    with pytest.raises(ValueError, match="decoder"):
        decoder2to4(a, b)
