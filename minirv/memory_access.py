"""Validação de acesso a memória compartilhada pelas memórias de instruções e de dados (Semana 06)."""
from minirv.word32 import MASK32

LARGURA_PALAVRA = 4  # bytes


class MemoryAccessError(ValueError):
    """Acesso inválido; a mensagem sempre traz memória, endereço e causa."""


def validar_endereco(nome, endereco, tamanho_bytes):
    if isinstance(endereco, bool) or not isinstance(endereco, int):
        raise MemoryAccessError(f"[{nome}] acesso inválido no endereço {endereco!r}: endereço não é inteiro")
    rotulo = f"{endereco} (0x{endereco & MASK32:08X})" if endereco >= 0 else f"{endereco}"
    if endereco < 0:
        raise MemoryAccessError(f"[{nome}] acesso inválido no endereço {rotulo}: abaixo do início da memória (0)")
    if endereco % LARGURA_PALAVRA != 0:
        raise MemoryAccessError(
            f"[{nome}] acesso inválido no endereço {rotulo}: desalinhado (múltiplo de 4 exigido)")
    ultimo = tamanho_bytes - LARGURA_PALAVRA
    if endereco > ultimo:
        raise MemoryAccessError(
            f"[{nome}] acesso inválido no endereço {rotulo}: acima do último endereço em que uma palavra "
            f"inteira cabe (0x{ultimo:08X}; tamanho {tamanho_bytes} bytes)")
