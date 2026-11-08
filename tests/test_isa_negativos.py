"""Casos negativos: nada é aceito em silêncio (registrador, imediato, opcode/funct, campos)."""
import json
from pathlib import Path

import pytest

import minirv.isa as isa
from minirv.decoder import decode
from minirv.encoder import encode

CASOS = json.loads((Path(__file__).parent / "vectors" / "rv32i-v1-negativos.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("c", CASOS, ids=[c["descricao"] for c in CASOS])
def test_caso_negativo(c):
    erro = getattr(isa, c["erro"])
    entrada = c["entrada"]
    if c["operacao"] == "encode":
        chamada = lambda: encode(entrada)
    else:
        palavra = entrada["raw"] if isinstance(entrada, dict) else int(entrada, 16)
        chamada = lambda: decode(palavra)
    with pytest.raises(erro) as e:
        chamada()
    assert c["mensagem"] in str(e.value)
    assert isinstance(e.value, isa.ISAError) and isinstance(e.value, ValueError)


def test_os_tres_casos_negativos_obrigatorios_estao_presentes():
    erros = {c["erro"] for c in CASOS}
    assert {"InvalidRegisterError", "ImmediateRangeError", "UnsupportedInstructionError"} <= erros


@pytest.mark.parametrize("palavra", [None, 1.5, True, -1, 1 << 32, [0x13]])
def test_decode_palavra_que_nao_e_inteiro_de_32_bits(palavra):
    with pytest.raises(isa.InvalidWordError):
        decode(palavra)


@pytest.mark.parametrize("instr", [None, "ADD", 5, ["ADD"]])
def test_encode_entrada_que_nao_e_dict(instr):
    with pytest.raises(isa.FieldMismatchError):
        encode(instr)


def test_encode_nao_altera_a_entrada():
    instr = {"mnemonic": "ADD", "rd": 1, "rs1": 2, "rs2": 3}
    copia = dict(instr)
    encode(instr)
    assert instr == copia
