"""Vetores válidos (um ou mais por instrução): palavra produzida e volta por decode."""
import json
from pathlib import Path

import pytest

from minirv.decoder import decode, format_assembly
from minirv.encoder import encode
from minirv.isa import OBRIGATORIAS

VETORES = json.loads((Path(__file__).parent / "vectors" / "rv32i-v1.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("v", VETORES, ids=[v["assembly"] for v in VETORES])
def test_encode_produz_a_palavra_do_vetor(v):
    assert encode(v["expected"]) == int(v["word"], 16)


@pytest.mark.parametrize("v", VETORES, ids=[v["assembly"] for v in VETORES])
def test_decode_devolve_os_campos_esperados(v):
    assert decode(int(v["word"], 16)) == v["expected"]


@pytest.mark.parametrize("v", VETORES, ids=[v["assembly"] for v in VETORES])
def test_assembly_do_vetor_e_a_sintaxe_canonica(v):
    assert format_assembly(v["expected"]) == v["assembly"]


def test_cada_uma_das_19_instrucoes_tem_ao_menos_um_vetor():
    cobertas = {v["expected"]["mnemonic"] for v in VETORES}
    assert cobertas == set(OBRIGATORIAS) and len(OBRIGATORIAS) == 19


def test_vetores_sem_duplicatas_e_palavras_de_32_bits():
    assert len({v["assembly"] for v in VETORES}) == len(VETORES)
    assert all(0 <= int(v["word"], 16) <= 0xFFFFFFFF and v["word"].startswith("0x") for v in VETORES)


def test_exemplo_do_guia():
    assert encode({"mnemonic": "ADD", "rd": 3, "rs1": 1, "rs2": 2}) == 0x002081B3
    assert decode(0x002081B3) == {"mnemonic": "ADD", "format": "R", "rd": 3, "rs1": 1, "rs2": 2}


def test_campos_que_nao_pertencem_ao_formato_nao_aparecem():
    assert "rd" not in decode(int(next(v for v in VETORES if v["assembly"].startswith("SW"))["word"], 16))
    lui = decode(0xFFFF0537)
    assert "rs1" not in lui and "rs2" not in lui and lui["imm"] == 0xFFFF0
