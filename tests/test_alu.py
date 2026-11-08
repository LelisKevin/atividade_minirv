import pytest

from minirv.alu import execute


def test_add_basico():
    assert execute("ADD", 5, 7) == 12


def test_add_zero():
    assert execute("ADD", 0, 0) == 0


def test_operacao_desconhecida():
    with pytest.raises(ValueError, match="desconhecida"):
        execute("MUL", 1, 2)
