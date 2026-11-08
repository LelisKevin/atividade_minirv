"""Banco de 32 registradores x0-x31: duas leituras, uma escrita, x0 imutável (Semanas 01 e 05)."""
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

    def read2(self, rs1, rs2):
        """Duas leituras simultâneas, sem alterar o estado."""
        return self.read(rs1), self.read(rs2)

    def write(self, rd, value, enable=True):
        """Grava value (normalizado para 32 bits) em rd.

        rd é sempre validado. Com enable=False o estado é mantido; escrita em x0 é ignorada.
        """
        self._check(rd)
        if not isinstance(enable, bool):
            raise ValueError(f"enable deve ser bool: {enable!r}")
        value = normalizar32(value)
        if not enable or rd == 0:
            return
        self._regs[rd] = value

    def dump(self):
        return {f"x{i}": v for i, v in enumerate(self._regs)}
