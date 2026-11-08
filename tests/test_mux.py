import pytest

from minirv.combinacional.mux import mux2


def test_sel_0_escolhe_entrada0():
    assert mux2(0, 10, 99) == 10


def test_sel_1_escolhe_entrada1():
    assert mux2(1, 10, 99) == 99


def test_seletor_nao_modifica_os_dados():
    obj0, obj1 = object(), object()
    assert mux2(0, obj0, obj1) is obj0
    assert mux2(1, obj0, obj1) is obj1


@pytest.mark.parametrize("sel", [2, -1, None, "0", 1.0, True])
def test_seletor_invalido(sel):
    with pytest.raises(ValueError, match="sel inválido"):
        mux2(sel, 10, 99)
