"""Program Counter de 32 bits (Semana 05): avanço de 4 bytes, salto validado e reset."""
from minirv.word32 import MASK32, normalizar32

PASSO = 4


class ProgramCounter:
    def __init__(self, valor_inicial=0):
        self._valor_inicial = self._validar(valor_inicial)
        self._pc = self._valor_inicial

    @staticmethod
    def _validar(alvo):
        if isinstance(alvo, bool) or not isinstance(alvo, int):
            raise ValueError(f"alvo de PC deve ser inteiro: {alvo!r}")
        if not 0 <= alvo <= MASK32:
            raise ValueError(f"alvo de PC fora de 32 bits: {alvo}")
        if alvo % PASSO != 0:
            raise ValueError(f"alvo de PC desalinhado (múltiplo de 4 exigido): 0x{alvo:08X}")
        return alvo

    def value(self):
        return self._pc

    def advance(self):
        """PC <- PC + 4, limitado a 32 bits (0xFFFFFFFC + 4 = 0)."""
        self._pc = normalizar32(self._pc + PASSO)

    def jump(self, target):
        """Carrega um endereço-alvo válido (inteiro, 32 bits, alinhado em 4)."""
        self._pc = self._validar(target)

    def reset(self):
        self._pc = self._valor_inicial
