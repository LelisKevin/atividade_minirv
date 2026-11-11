"""Memória de dados com RAM e registradores MMIO: palavras de 32 bits little-endian.

Valida endereço inteiro, alinhado em 4 e dentro da faixa. Todo acesso inválido gera MemoryAccessError
com endereço e causa; nunca há truncamento de endereço nem escrita parcial. Os registradores MMIO
são exceções explícitas à faixa da RAM e aceitam leitura e escrita.
"""
from minirv.memory_access import LARGURA_PALAVRA, MemoryAccessError, validar_endereco  # noqa: F401
from minirv.word32 import normalizar32

NOME = "memória de dados"
TAMANHO_PADRAO = 4096  # bytes (ADR-001)
IO_INPUT = 0x80000000
IO_SIGNAL = 0x80000004
IO_CYCLES = 0x80000008


class DataMemory:
    def __init__(self, size_bytes=TAMANHO_PADRAO):
        if isinstance(size_bytes, bool) or not isinstance(size_bytes, int) or size_bytes <= 0 \
                or size_bytes % LARGURA_PALAVRA:
            raise ValueError(f"tamanho inválido: {size_bytes!r} (inteiro positivo, múltiplo de 4)")
        self._bytes = bytearray(size_bytes)
        self.io_input = 0
        self.io_signal = 0
        self.io_cycles = 0

    @property
    def size_bytes(self):
        return len(self._bytes)

    def read_word(self, address):
        if isinstance(address, int) and not isinstance(address, bool):
            if address == IO_INPUT:
                return self.io_input
            if address == IO_SIGNAL:
                return self.io_signal
            if address == IO_CYCLES:
                return self.io_cycles

        validar_endereco(NOME, address, self.size_bytes)
        return int.from_bytes(self._bytes[address:address + LARGURA_PALAVRA], "little")

    def write_word(self, address, value):
        if isinstance(address, int) and not isinstance(address, bool):
            if address == IO_INPUT:
                self.io_input = normalizar32(value)
                return
            if address == IO_SIGNAL:
                self.io_signal = normalizar32(value)
                return
            if address == IO_CYCLES:
                self.io_cycles = normalizar32(value)
                return

        validar_endereco(NOME, address, self.size_bytes)
        valor = normalizar32(value)  # valida inteiro antes de tocar na memória
        self._bytes[address:address + LARGURA_PALAVRA] = valor.to_bytes(LARGURA_PALAVRA, "little")
