import pytest

from minirv.decoder import decode, format_assembly


def test_decode_addi():
    assert decode(0x00500093) == {"mnemonic": "ADDI", "format": "I", "rd": 1, "rs1": 0, "imm": 5}


def test_decode_addi_negativo():
    assert decode(0xFFF00093)["imm"] == -1


def test_decode_add():
    assert decode(0x002081B3) == {"mnemonic": "ADD", "format": "R", "rd": 3, "rs1": 1, "rs2": 2}


def test_instrucao_nao_suportada():
    with pytest.raises(ValueError, match="não suportada"):
        decode(0x00000073)  # ecall


def test_palavra_invalida():
    with pytest.raises(ValueError):
        decode(1 << 32)


def test_format_assembly():
    assert format_assembly(decode(0x002081B3)) == "ADD x3, x1, x2"
