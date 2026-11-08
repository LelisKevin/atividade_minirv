from pathlib import Path

import pytest

from minirv.combinacional.control import decode_control

ROOT = Path(__file__).resolve().parent.parent
SINAIS = ("RegWrite", "ALUSrc", "MemRead", "MemWrite", "Branch")


def test_store_grava_memoria_e_nao_grava_registrador():
    sinais = decode_control(0b0100011)
    assert sinais["MemWrite"] == 1
    assert sinais["RegWrite"] == 0


def test_load_le_memoria_e_grava_registrador():
    s = decode_control(0b0000011)
    assert (s["MemRead"], s["RegWrite"], s["ALUSrc"]) == (1, 1, 1)


def test_branch_so_habilita_desvio():
    s = decode_control(0b1100011)
    assert s["Branch"] == 1 and s["RegWrite"] == 0 and s["MemWrite"] == 0 and s["ALUSrc"] == 0


def test_classes():
    assert [decode_control(o)["classe"] for o in (0b0110011, 0b0010011, 0b0000011, 0b0100011, 0b1100011)] == \
           ["R", "I", "LOAD", "STORE", "BRANCH"]


@pytest.mark.parametrize("opcode", [0b0000000, 0b1111111, 0b1101111, 0b0110111, 0b1100111])
def test_opcode_nao_suportado(opcode):
    with pytest.raises(ValueError, match="Opcode não suportado"):
        decode_control(opcode)


@pytest.mark.parametrize("opcode", [None, "0110011", 51.0])
def test_opcode_nao_inteiro(opcode):
    with pytest.raises(ValueError, match="inteiro"):
        decode_control(opcode)


def test_alterar_o_resultado_nao_altera_a_tabela():
    s = decode_control(0b0110011)
    s["RegWrite"] = 0
    assert decode_control(0b0110011)["RegWrite"] == 1


def test_tabela_documentada_coincide_com_o_codigo():
    """docs/logica/sinais-controle.md é a especificação; a função deve reproduzi-la."""
    classe_de = {"ADD": 0b0110011, "ADDI": 0b0010011, "LW": 0b0000011, "SW": 0b0100011, "BEQ": 0b1100011}
    texto = (ROOT / "docs/logica/sinais-controle.md").read_text(encoding="utf-8")
    encontrados = 0
    for linha in texto.splitlines():
        cel = [c.strip() for c in linha.strip("|").split("|")]
        if linha.startswith("| ") and cel[0] in classe_de and len(cel) == 7:
            esperado = dict(zip(SINAIS, map(int, cel[2:])))
            obtido = {k: v for k, v in decode_control(classe_de[cel[0]]).items() if k in SINAIS}
            assert obtido == esperado, cel[0]
            encontrados += 1
    assert encontrados == 5
