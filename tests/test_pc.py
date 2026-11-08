import pytest

from minirv.alu import execute
from minirv.pc import ProgramCounter


def test_sequencia_do_guia():
    pc = ProgramCounter()
    pc.reset()
    assert pc.value() == 0x00000000
    pc.advance()
    assert pc.value() == 0x00000004
    pc.advance()
    assert pc.value() == 0x00000008
    pc.jump(0x00000100)
    assert pc.value() == 0x00000100
    pc.advance()
    assert pc.value() == 0x00000104
    pc.reset()
    assert pc.value() == 0x00000000


def test_inicia_em_zero():
    assert ProgramCounter().value() == 0


def test_avanco_limitado_a_32_bits():
    pc = ProgramCounter()
    pc.jump(0xFFFFFFFC)
    pc.advance()
    assert pc.value() == 0


@pytest.mark.parametrize("alvo", [-4, 2, 0x102, 1 << 32, 0x1_0000_0000, "0x100", None, 1.0, True])
def test_jump_invalido_gera_erro_e_preserva_estado(alvo):
    pc = ProgramCounter()
    pc.jump(0x20)
    with pytest.raises(ValueError, match="alvo de PC"):
        pc.jump(alvo)
    assert pc.value() == 0x20


def test_reset_volta_ao_valor_inicial_configurado():
    pc = ProgramCounter(valor_inicial=0x400)
    pc.advance()
    pc.reset()
    assert pc.value() == 0x400


# ---- Desvios por composição: ALU decide, PC obedece (a lógica de controle completa vem depois) ----
def aplicar_desvio(pc, condicao, alvo):
    if condicao:
        pc.jump(alvo)
    else:
        pc.advance()


def beq(a, b):
    return execute("SUB", a, b) == 0  # igualdade: SUB resulta em zero


def bne(a, b):
    return execute("SUB", a, b) != 0


def blt(a, b):
    return execute("SLT", a, b) == 1  # comparação com sinal


@pytest.mark.parametrize("a,b,tomado", [(5, 5, True), (5, 6, False), (0, 0, True), (-1, -1, True), (-1, 1, False)])
def test_beq_por_composicao(a, b, tomado):
    pc = ProgramCounter(); pc.jump(0x20)
    aplicar_desvio(pc, beq(a, b), 0x100)
    assert pc.value() == (0x100 if tomado else 0x24)


@pytest.mark.parametrize("a,b,tomado", [(5, 6, True), (5, 5, False), (-1, 1, True), (1, -1, False), (0x80000000, 0, True)])
def test_blt_com_sinal_por_composicao(a, b, tomado):
    pc = ProgramCounter(); pc.jump(0x20)
    aplicar_desvio(pc, blt(a, b), 0x100)
    assert pc.value() == (0x100 if tomado else 0x24)


def test_bne_e_o_inverso_do_beq():
    for a, b in [(1, 1), (1, 2), (-1, 0xFFFFFFFF), (0, 0x80000000)]:
        assert bne(a, b) != beq(a, b)
