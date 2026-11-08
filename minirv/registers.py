"""Banco de registradores x0-x31 (Semana 01). x0 é sempre zero."""

NUM_REGISTERS = 32
MASK32 = 0xFFFFFFFF


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
        """Grava value & 0xFFFFFFFF. Escrita em x0 é ignorada."""
        self._check(index)
        if index == 0:
            return
        self._regs[index] = value & MASK32

    def dump(self):
        return {f"x{i}": v for i, v in enumerate(self._regs)}
