import pytest

from minirv.registers import RegisterFile


def test_inicializa_zerado():
    r = RegisterFile()
    assert all(r.read(i) == 0 for i in range(32))


def test_x0_nao_muda():
    r = RegisterFile()
    r.write(0, 123)
    assert r.read(0) == 0


def test_escreve_e_le():
    r = RegisterFile()
    r.write(5, 10)
    assert r.read(5) == 10


@pytest.mark.parametrize("idx", [-1, 32, 100, "x1", 1.0, None, True])
def test_indice_invalido_gera_erro(idx):
    with pytest.raises(ValueError, match="registrador inválido"):
        RegisterFile().read(idx)
