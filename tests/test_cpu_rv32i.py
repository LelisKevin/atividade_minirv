import pytest

from minirv.cpu import CPU
from minirv.encoder import encode
from minirv.word32 import MASK32


@pytest.mark.parametrize(
    "mnemonic,a,b,esperado",
    [
        ("SUB", 3, 5, MASK32 - 1),
        ("SLL", 3, 2, 12),
        ("SLT", 0x80000000, 1, 1),
        ("XOR", 0xAA55, 0x0FF0, 0xA5A5),
        ("SRL", 0x80000000, 1, 0x40000000),
        ("OR", 0xA0, 0x0A, 0xAA),
        ("AND", 0xAA, 0x0F, 0x0A),
    ],
)
def test_cpu_executa_operacoes_r(mnemonic, a, b, esperado):
    cpu = CPU([encode({"mnemonic": mnemonic, "rd": 3, "rs1": 1, "rs2": 2})])
    cpu.regs.write(1, a)
    cpu.regs.write(2, b)

    cpu.step()

    assert cpu.regs.read(3) == esperado


@pytest.mark.parametrize(
    "mnemonic,a,imm,esperado",
    [
        ("ORI", 0x1000, -1, MASK32),
        ("ANDI", 0xFFFF0FFF, -2048, 0xFFFF0800),
    ],
)
def test_cpu_executa_operacoes_imediatas_com_extensao_de_sinal(mnemonic, a, imm, esperado):
    cpu = CPU([encode({"mnemonic": mnemonic, "rd": 3, "rs1": 1, "imm": imm})])
    cpu.regs.write(1, a)

    cpu.step()

    assert cpu.regs.read(3) == esperado


@pytest.mark.parametrize(
    "mnemonic,a,b,tomado",
    [
        ("BEQ", 5, 5, True),
        ("BEQ", 5, 6, False),
        ("BNE", 5, 6, True),
        ("BNE", 5, 5, False),
        ("BLT", 0xFFFFFFFF, 1, True),
        ("BLT", 1, 0xFFFFFFFF, False),
        ("BLT", 0x80000000, 0x7FFFFFFF, True),
    ],
)
def test_cpu_executa_desvios(mnemonic, a, b, tomado):
    instrucao = encode({"mnemonic": mnemonic, "rs1": 1, "rs2": 2, "imm": 8})
    cpu = CPU([instrucao, 0x00000013, 0x00000013])
    cpu.regs.write(1, a)
    cpu.regs.write(2, b)

    registro = cpu.step()

    assert cpu.pc == (8 if tomado else 4)
    assert registro["next_pc"] == f"0x{cpu.pc:08X}"


def test_cpu_jalr_salva_link_e_limpa_bit_zero_do_alvo():
    cpu = CPU([encode({"mnemonic": "JALR", "rd": 5, "rs1": 1, "imm": 3})])
    cpu.regs.write(1, 0x22)

    cpu.step()

    assert cpu.pc == 0x24
    assert cpu.regs.read(5) == 4


def test_cpu_jalr_com_alvo_desalinhado_nao_altera_link_ou_pc():
    cpu = CPU([encode({"mnemonic": "JALR", "rd": 5, "rs1": 1, "imm": 0})])
    cpu.regs.write(1, 0x22)

    with pytest.raises(ValueError, match="desalinhado"):
        cpu.step()

    assert cpu.pc == 0
    assert cpu.regs.read(5) == 0
    assert cpu.instruction_count == 0


def test_cpu_executa_todas_as_19_instrucoes_do_contrato():
    instrucoes = [
        {"mnemonic": "ADD", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "SUB", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "SLL", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "SLT", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "XOR", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "SRL", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "OR", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "AND", "rd": 3, "rs1": 1, "rs2": 2},
        {"mnemonic": "ADDI", "rd": 3, "rs1": 1, "imm": 1},
        {"mnemonic": "ORI", "rd": 3, "rs1": 1, "imm": 1},
        {"mnemonic": "ANDI", "rd": 3, "rs1": 1, "imm": 1},
        {"mnemonic": "LW", "rd": 3, "rs1": 1, "imm": 0},
        {"mnemonic": "JALR", "rd": 0, "rs1": 0, "imm": 0},
        {"mnemonic": "SW", "rs1": 1, "rs2": 2, "imm": 0},
        {"mnemonic": "BEQ", "rs1": 0, "rs2": 0, "imm": 4},
        {"mnemonic": "BNE", "rs1": 1, "rs2": 2, "imm": 4},
        {"mnemonic": "BLT", "rs1": 1, "rs2": 2, "imm": 4},
        {"mnemonic": "JAL", "rd": 0, "imm": 0},
        {"mnemonic": "LUI", "rd": 3, "imm": 1},
    ]
    assert len({instrucao["mnemonic"] for instrucao in instrucoes}) == 19
    for instrucao in instrucoes:
        cpu = CPU([encode(instrucao)])
        cpu.regs.write(1, 0)
        cpu.regs.write(2, 0)
        cpu.memory.write_word(0, 0x12345678)

        assert cpu.step()["instruction"].startswith(instrucao["mnemonic"])
        assert cpu.instruction_count == 1
