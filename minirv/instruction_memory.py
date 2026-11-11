"""Memória de instruções (Semana 06): somente leitura de palavras de 32 bits, endereçada por byte."""
from minirv.memory_access import LARGURA_PALAVRA, validar_endereco
from minirv.word32 import MASK32

NOME = "memória de instruções"


class InstructionMemory:
    def __init__(self, palavras):
        palavras = list(palavras)
        for i, w in enumerate(palavras):
            if isinstance(w, bool) or not isinstance(w, int) or not 0 <= w <= MASK32:
                raise ValueError(f"palavra {i} inválida (esperado inteiro de 32 bits): {w!r}")
        self._palavras = palavras

    @property
    def size_bytes(self):
        return len(self._palavras) * LARGURA_PALAVRA

    def read_word(self, pc):
        validar_endereco(NOME, pc, self.size_bytes)
        return self._palavras[pc // LARGURA_PALAVRA]

    