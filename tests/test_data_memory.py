import pytest

from minirv.data_memory import DataMemory, MemoryAccessError

TAM = 64


@pytest.fixture
def mem():
    return DataMemory(TAM)


def test_inicia_zerada(mem):
    assert all(mem.read_word(a) == 0 for a in range(0, TAM, 4))


def test_leitura_escrita_valida_e_alinhada(mem):
    mem.write_word(0, 12)
    mem.write_word(TAM - 4, 0xDEADBEEF)  # último endereço em que cabe uma palavra
    assert mem.read_word(0) == 12
    assert mem.read_word(TAM - 4) == 0xDEADBEEF
    assert mem.read_word(4) == 0


def test_little_endian_por_byte(mem):
    mem.write_word(8, 0x11223344)
    assert [mem.read_word(8) >> s & 0xFF for s in (0, 8, 16, 24)] == [0x44, 0x33, 0x22, 0x11]


def test_valor_e_normalizado_para_32_bits(mem):
    mem.write_word(0, -1)
    assert mem.read_word(0) == 0xFFFFFFFF
    mem.write_word(0, (1 << 32) + 5)
    assert mem.read_word(0) == 5


@pytest.mark.parametrize("addr,causa", [
    (6, "desalinhado"), (1, "desalinhado"), (TAM - 2, "desalinhado"),
    (-4, "abaixo do início"), (-1, "abaixo do início"),
    (TAM, "acima do último"), (TAM + 4, "acima do último"), (2**32, "acima do último"),
])
def test_acesso_invalido_tem_endereco_e_causa(mem, addr, causa):
    for operacao in (lambda: mem.read_word(addr), lambda: mem.write_word(addr, 1)):
        with pytest.raises(MemoryAccessError) as e:
            operacao()
        assert str(addr) in str(e.value) and causa in str(e.value) and "memória de dados" in str(e.value)


@pytest.mark.parametrize("addr", [1.5, "4", None, True])
def test_endereco_nao_inteiro(mem, addr):
    with pytest.raises(MemoryAccessError, match="não é inteiro"):
        mem.read_word(addr)


def test_nao_ha_escrita_parcial_nem_truncamento(mem):
    mem.write_word(TAM - 4, 0xAAAAAAAA)
    for addr in (TAM - 2, TAM, TAM + 2):
        with pytest.raises(MemoryAccessError):
            mem.write_word(addr, 0x55555555)
    assert mem.read_word(TAM - 4) == 0xAAAAAAAA
    assert mem.read_word(0) == 0
    with pytest.raises(MemoryAccessError):  # 2**32 não vira endereço 0
        mem.write_word(2**32, 7)
    assert mem.read_word(0) == 0


def test_valor_invalido_nao_altera_memoria(mem):
    mem.write_word(0, 9)
    with pytest.raises(ValueError):
        mem.write_word(0, 1.5)
    assert mem.read_word(0) == 9


@pytest.mark.parametrize("tam", [0, -4, 6, 1.0, None, True])
def test_tamanho_invalido(tam):
    with pytest.raises(ValueError, match="tamanho inválido"):
        DataMemory(tam)


def test_tamanho_padrao_4kib():
    assert DataMemory().size_bytes == 4096
