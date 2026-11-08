import pytest

from minirv.word32 import (
    estender_sinal, normalizar32, para_bin32, para_hex32, para_signed32, para_unsigned32, soma32,
)


def test_zero():
    assert para_unsigned32(0) == 0
    assert para_signed32(0) == 0
    assert para_hex32(0) == "0x00000000"


def test_menos_um():
    assert para_unsigned32(-1) == 0xFFFFFFFF
    assert para_signed32(-1) == -1
    assert para_hex32(-1) == "0xFFFFFFFF"


def test_maior_positivo():
    assert para_signed32(0x7FFFFFFF) == 2147483647
    assert para_signed32(2**31 - 1) == 2147483647


def test_menor_negativo():
    assert para_signed32(0x80000000) == -2147483648
    assert para_signed32(-(2**31)) == -2147483648
    assert para_hex32(-(2**31)) == "0x80000000"


def test_overflow_unsigned():
    assert soma32(0xFFFFFFFF, 1) == 0x00000000


def test_overflow_signed_da_soma():
    assert para_signed32(soma32(0x7FFFFFFF, 1)) == -2147483648


def test_binario():
    assert para_bin32(0x2A) == "00000000000000000000000000101010"
    assert int(para_bin32(0x2A), 2) == 42


def test_binario_sempre_32_digitos():
    assert len(para_bin32(0)) == 32 and len(para_bin32(-1)) == 32


def test_normalizar_descarta_bits_acima_de_32():
    assert normalizar32(1 << 32) == 0
    assert normalizar32((1 << 32) + 5) == 5
    assert normalizar32(-(2**40) - 1) == 0xFFFFFFFF


@pytest.mark.parametrize("valor,bits,esperado", [
    (0x7FF, 12, 0x000007FF),
    (0x800, 12, 0xFFFFF800),
    (0xFFF, 12, 0xFFFFFFFF),
    (0x1, 1, 0xFFFFFFFF),
    (0x0, 1, 0),
    (0x80, 8, 0xFFFFFF80),
    (0xDEADBEEF, 32, 0xDEADBEEF),
])
def test_estender_sinal(valor, bits, esperado):
    assert estender_sinal(valor, bits) == esperado


@pytest.mark.parametrize("entrada", [1.5, "3", None, True, [1]])
def test_entrada_nao_inteira_gera_erro(entrada):
    with pytest.raises(ValueError, match="inteiro"):
        normalizar32(entrada)


@pytest.mark.parametrize("bits", [0, 33, -1, True, 2.0])
def test_estender_sinal_bits_invalido(bits):
    with pytest.raises(ValueError, match="bits_origem"):
        estender_sinal(1, bits)


def test_registrador_normaliza_na_escrita():
    from minirv.registers import RegisterFile
    r = RegisterFile()
    r.write(3, -1)
    assert r.read(3) == 0xFFFFFFFF
    r.write(4, 1 << 33)
    assert r.read(4) == 0
