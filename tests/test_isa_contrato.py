"""O contrato (docs/isa/rv32i-subset-v1.md) é a fonte única: estrutura, consistência e leitura rigorosa."""
import re
from pathlib import Path

import pytest

from minirv.isa import CONTRATO, FIM, INICIO, OBRIGATORIAS, SPEC, load_spec

# Codificações do RISC-V Unprivileged ISA (RV32I), digitadas de forma independente do contrato:
CANONICO = {
    "ADD": (0b0110011, 0b000, 0b0000000), "SUB": (0b0110011, 0b000, 0b0100000),
    "SLL": (0b0110011, 0b001, 0b0000000), "SLT": (0b0110011, 0b010, 0b0000000),
    "XOR": (0b0110011, 0b100, 0b0000000), "SRL": (0b0110011, 0b101, 0b0000000),
    "OR": (0b0110011, 0b110, 0b0000000), "AND": (0b0110011, 0b111, 0b0000000),
    "ADDI": (0b0010011, 0b000, None), "ORI": (0b0010011, 0b110, None), "ANDI": (0b0010011, 0b111, None),
    "LW": (0b0000011, 0b010, None), "JALR": (0b1100111, 0b000, None), "SW": (0b0100011, 0b010, None),
    "BEQ": (0b1100011, 0b000, None), "BNE": (0b1100011, 0b001, None), "BLT": (0b1100011, 0b100, None),
    "JAL": (0b1101111, None, None), "LUI": (0b0110111, None, None),
}
FORMATO = {"R": ["ADD", "SUB", "SLL", "SLT", "XOR", "SRL", "OR", "AND"], "I": ["ADDI", "ORI", "ANDI", "LW", "JALR"],
           "S": ["SW"], "B": ["BEQ", "BNE", "BLT"], "U": ["LUI"], "J": ["JAL"]}
TEXTO = CONTRATO.read_text(encoding="utf-8")


def test_19_instrucoes_obrigatorias():
    assert len(OBRIGATORIAS) == 19 and set(SPEC) == set(OBRIGATORIAS)


@pytest.mark.parametrize("m", sorted(CANONICO))
def test_codificacao_do_contrato_coincide_com_o_manual_riscv(m):
    s = SPEC[m]
    assert (s.opcode, s.funct3, s.funct7) == CANONICO[m]


def test_formatos_do_contrato():
    for fmt, ms in FORMATO.items():
        assert all(SPEC[m].format == fmt for m in ms)
    assert sum(len(v) for v in FORMATO.values()) == 19


def test_faixas_do_contrato():
    assert (SPEC["ADDI"].imm_min, SPEC["ADDI"].imm_max) == (-2048, 2047)
    assert (SPEC["BEQ"].imm_min, SPEC["BEQ"].imm_max, SPEC["BEQ"].imm_align) == (-4096, 4092, 4)
    assert (SPEC["JAL"].imm_min, SPEC["JAL"].imm_max, SPEC["JAL"].imm_align) == (-1048576, 1048572, 4)
    assert (SPEC["LUI"].imm_min, SPEC["LUI"].imm_max) == (0, 0xFFFFF)


@pytest.mark.parametrize("fmt", ["R", "I", "S", "B", "U", "J"])
def test_layout_de_cada_formato_esta_documentado_com_posicao_e_largura(fmt):
    secao = re.search(rf"\*\*{fmt}\*\* — `([^`]+)`\n\n\| Campo.*?\n\| ---.*?\n\| Bits \|([^\n]+)\n\| Largura \|([^\n]+)\n",
                      TEXTO, re.S)
    assert secao, f"layout {fmt} sem tabela de bits/largura"
    larguras = [int(x) for x in secao.group(3).strip().strip("|").split("|")]
    assert sum(larguras) == 32  # as larguras documentadas fecham 32 bits


def test_secoes_obrigatorias_do_contrato():
    for titulo in ("## 2. Layouts", "## 3. Tabela de codificação", "## 4. Sintaxe", "## 5. Mensagens de erro",
                   "## 6. Impacto da regularidade", "## 8. Versão, congelamento"):
        assert titulo in TEXTO
    assert "fonte única de verdade" in TEXTO


def test_status_de_congelamento_esta_explicito():
    assert re.search(r"Status: v1 (CONGELADA|CANDIDATA A CONGELAMENTO)", TEXTO)


def test_regularidade_nao_afirma_superioridade_universal():
    secao = TEXTO.split("## 6. Impacto da regularidade")[1].split("## 7.")[0]
    assert "não afirma que um dos estilos seja superior em geral" in secao
    for tema in ("Decodificação", "Caminho de dados", "Instruções por operação", "Tamanho do código", "testar"):
        assert tema in secao


# ---- leitura rigorosa do contrato ----
def _com(tmp_path, nova):
    p = tmp_path / "c.md"
    p.write_text(nova, encoding="utf-8")
    return p


def test_load_spec_rejeita_marcadores_ausentes(tmp_path):
    with pytest.raises(ValueError, match="marcadores"):
        load_spec(_com(tmp_path, "sem tabela"))


def test_load_spec_rejeita_instrucao_faltando(tmp_path):
    linhas = [l for l in TEXTO.splitlines() if not l.startswith("| LUI ")]
    with pytest.raises(ValueError, match="faltando"):
        load_spec(_com(tmp_path, "\n".join(linhas)))


def test_load_spec_rejeita_mnemonico_duplicado(tmp_path):
    linha = next(l for l in TEXTO.splitlines() if l.startswith("| ADD "))
    with pytest.raises(ValueError, match="duplicado"):
        load_spec(_com(tmp_path, TEXTO.replace(INICIO, INICIO + "\n" + "\n".join([]) ).replace(linha, linha + "\n" + linha)))


def test_load_spec_rejeita_opcode_com_largura_errada(tmp_path):
    with pytest.raises(ValueError, match="7 bits"):
        load_spec(_com(tmp_path, TEXTO.replace("| 0110111 |", "| 011011 |")))


def test_load_spec_rejeita_instrucao_a_mais(tmp_path):
    extra = "| MUL | R | MUL rd, rs1, rs2 | 0110011 | 000 | 0000001 | rd, rs1, rs2 | — | x | x |"
    with pytest.raises(ValueError, match="a mais"):
        load_spec(_com(tmp_path, TEXTO.replace(FIM, extra + "\n" + FIM)))


def test_alterar_o_contrato_altera_a_especificacao(tmp_path):
    """Prova de que a tabela é a fonte única: trocar o funct3 do ORI no .md muda o que o código lê."""
    alterado = TEXTO.replace("| ORI | I | ORI rd, rs1, imm | 0010011 | 110 |", "| ORI | I | ORI rd, rs1, imm | 0010011 | 011 |")
    assert load_spec(_com(tmp_path, alterado))["ORI"].funct3 == 0b011
    assert SPEC["ORI"].funct3 == 0b110
