"""Palavra de 32 bits (Semana 03).

A linguagem hospedeira aceita inteiros de qualquer tamanho; o simulador não pode depender disso.
Toda grandeza arquitetural passa por normalizar32 (máscara 0xFFFFFFFF), que preserva apenas
os 32 bits menos significativos.
"""

MASK32 = 0xFFFFFFFF


def _inteiro(valor):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"valor deve ser inteiro: {valor!r}")
    return valor


def normalizar32(valor):
    """Mantém apenas os 32 bits menos significativos (resultado em 0..0xFFFFFFFF)."""
    return _inteiro(valor) & MASK32


def para_unsigned32(valor):
    """Interpretação sem sinal: 0 .. 4.294.967.295."""
    return normalizar32(valor)


def para_signed32(valor):
    """Interpretação em complemento de dois: -2.147.483.648 .. 2.147.483.647."""
    valor = normalizar32(valor)
    if valor & 0x80000000:
        return valor - 0x100000000
    return valor


def para_hex32(valor):
    """Oito dígitos hexadecimais com prefixo 0x."""
    return f"0x{normalizar32(valor):08X}"


def para_bin32(valor):
    """Sempre 32 dígitos binários."""
    return f"{normalizar32(valor):032b}"


def estender_sinal(valor, bits_origem):
    """Amplia um padrão de bits_origem bits para 32 bits preservando o sinal."""
    if not isinstance(bits_origem, int) or isinstance(bits_origem, bool) or not 1 <= bits_origem <= 32:
        raise ValueError(f"bits_origem deve estar entre 1 e 32: {bits_origem!r}")
    mascara = (1 << bits_origem) - 1
    valor = _inteiro(valor) & mascara
    if valor & (1 << (bits_origem - 1)):
        valor -= 1 << bits_origem
    return normalizar32(valor)


def soma32(a, b):
    """Soma com overflow em 32 bits (0xFFFFFFFF + 1 = 0)."""
    return normalizar32(_inteiro(a) + _inteiro(b))
