"""Memória de dados (Semana 06): endereçada por byte, palavras de 32 bits little-endian.

Valida endereço inteiro, alinhado em 4 e dentro da faixa. Todo acesso inválido gera MemoryAccessError
com endereço e causa; nunca há truncamento de endereço nem escrita parcial.
"""
from minirv.memory_access import LARGURA_PALAVRA, MemoryAccessError, validar_endereco  # noqa: F401
from minirv.word32 import normalizar32

NOME = "memória de dados"
TAMANHO_PADRAO = 4096  # bytes (ADR-001)


class DataMemory:
    def __init__(self, size_bytes=TAMANHO_PADRAO):
        if isinstance(size_bytes, bool) or not isinstance(size_bytes, int) or size_bytes <= 0 \
                or size_bytes % LARGURA_PALAVRA:
            raise ValueError(f"tamanho inválido: {size_bytes!r} (inteiro positivo, múltiplo de 4)")
        self._bytes = bytearray(size_bytes)

    @property
    def size_bytes(self):
        return len(self._bytes)

    def read_word(self, address):
        validar_endereco(NOME, address, self.size_bytes)
        return int.from_bytes(self._bytes[address:address + LARGURA_PALAVRA], "little")

    def write_word(self, address, value):
        validar_endereco(NOME, address, self.size_bytes)
        valor = normalizar32(value)  # valida inteiro antes de tocar na memória
        self._bytes[address:address + LARGURA_PALAVRA] = valor.to_bytes(LARGURA_PALAVRA, "little")
