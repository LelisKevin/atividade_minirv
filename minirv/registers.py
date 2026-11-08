"""Banco de registradores x0-x31 (Semana 01). x0 é sempre zero."""

from minirv.word32 import normalizar32

NUM_REGISTERS = 32


class RegisterFile:
    def __init__(self):
        self._regs = [0] * NUM_REGISTERS

    @staticmethod
    def _check(index):
        if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < NUM_REGISTERS:
            raise ValueError(f"registrador inválido: {index!r} (válidos: 0 a 31)")

    def read(self, index):
        self._check(index)
        return self._regs[index]

    def write(self, index, value):
        """Grava value normalizado para 32 bits. Escrita em x0 é ignorada."""
        self._check(index)
        if index == 0:
            return
        self._regs[index] = normalizar32(value)

    def dump(self):
        return {f"x{i}": v for i, v in enumerate(self._regs)}
