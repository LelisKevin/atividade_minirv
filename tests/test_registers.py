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


# ---------------- Semana 05 ----------------
def test_x0_apos_inicializacao_e_escrita_de_123():
    r = RegisterFile()
    assert r.read(0) == 0
    r.write(0, 123)
    assert r.read(0) == 0


def test_escrita_em_x0_com_enable_tambem_ignorada():
    r = RegisterFile()
    r.write(0, 0xFFFFFFFF, enable=True)
    assert r.read(0) == 0


def test_escrever_x5_e_ler_valor_normalizado():
    r = RegisterFile()
    r.write(5, -1)
    assert r.read(5) == 0xFFFFFFFF
    r.write(5, (1 << 32) + 7)
    assert r.read(5) == 7


def test_enable_false_mantem_valor_anterior():
    r = RegisterFile()
    r.write(7, 42)
    r.write(7, 99, enable=False)
    assert r.read(7) == 42


def test_read2_nao_altera_estado_e_retorna_dois_operandos():
    r = RegisterFile()
    r.write(1, 5)
    r.write(2, 7)
    antes = r.dump()
    assert r.read2(1, 2) == (5, 7)
    assert r.read2(2, 2) == (7, 7)
    assert r.read2(0, 1) == (0, 5)
    assert r.dump() == antes


def test_escrita_nao_afeta_outros_registradores():
    r = RegisterFile()
    r.write(10, 1)
    assert [r.read(i) for i in range(32) if i != 10] == [0] * 31


@pytest.mark.parametrize("idx", [-1, 32, 99])
def test_indice_fora_de_0_31_em_todas_as_operacoes(idx):
    r = RegisterFile()
    with pytest.raises(ValueError, match="registrador inválido"):
        r.write(idx, 1)
    with pytest.raises(ValueError, match="registrador inválido"):
        r.write(idx, 1, enable=False)  # rd é validado mesmo sem escrita
    with pytest.raises(ValueError, match="registrador inválido"):
        r.read2(1, idx)
    with pytest.raises(ValueError, match="registrador inválido"):
        r.read2(idx, 1)


@pytest.mark.parametrize("enable", [1, 0, None, "sim"])
def test_enable_deve_ser_bool(enable):
    with pytest.raises(ValueError, match="enable"):
        RegisterFile().write(1, 1, enable=enable)


def test_escrita_com_valor_invalido():
    with pytest.raises(ValueError, match="inteiro"):
        RegisterFile().write(1, 1.5)
