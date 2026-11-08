import pytest

from minirv.instruction_memory import InstructionMemory
from minirv.memory_access import MemoryAccessError


def test_le_palavras_por_endereco_de_byte():
    m = InstructionMemory([0x11, 0x22, 0x33])
    assert [m.read_word(a) for a in (0, 4, 8)] == [0x11, 0x22, 0x33]
    assert m.size_bytes == 12


@pytest.mark.parametrize("pc,causa", [(2, "desalinhado"), (12, "acima do último"), (-4, "abaixo do início")])
def test_acesso_invalido(pc, causa):
    with pytest.raises(MemoryAccessError, match=causa):
        InstructionMemory([1, 2, 3]).read_word(pc)


@pytest.mark.parametrize("palavras", [[1 << 32], [-1], [1.5], [True]])
def test_palavra_invalida_na_construcao(palavras):
    with pytest.raises(ValueError, match="palavra 0 inválida"):
        InstructionMemory(palavras)


def test_vazia_nao_permite_leitura():
    with pytest.raises(MemoryAccessError):
        InstructionMemory([]).read_word(0)
