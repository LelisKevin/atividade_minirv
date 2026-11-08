import pytest

from minirv.alu import execute


def test_add_basico():
    assert execute("ADD", 5, 7) == 12


def test_add_zero():
    assert execute("ADD", 0, 0) == 0


def test_operacao_desconhecida():
    with pytest.raises(ValueError, match="desconhecida"):
        execute("MUL", 1, 2)


# ---------------- Semana 05: ULA completa ----------------
# Resultados esperados escritos à mão (não gerados pelo código).
CASOS = [
    # ADD: zero, normal, overflow, negativo + positivo, overflow com sinal, dois negativos
    ("ADD", 0, 0, 0),
    ("ADD", 5, 7, 12),
    ("ADD", 0xFFFFFFFF, 1, 0),
    ("ADD", -1, 5, 4),
    ("ADD", 0x7FFFFFFF, 1, 0x80000000),
    ("ADD", -1, -1, 0xFFFFFFFE),
    # SUB: normal, 0-1, mínimo-1, negativos, igual
    ("SUB", 7, 5, 2),
    ("SUB", 0, 1, 0xFFFFFFFF),
    ("SUB", 0x80000000, 1, 0x7FFFFFFF),
    ("SUB", -3, -5, 2),
    ("SUB", 5, 5, 0),
    # AND
    ("AND", 0xFFFFFFFF, 0, 0),
    ("AND", 0xAAAAAAAA, 0x55555555, 0),
    ("AND", 0xAAAAAAAA, 0xFFFFFFFF, 0xAAAAAAAA),
    # OR
    ("OR", 0, 0x1234, 0x1234),
    ("OR", 0xAAAAAAAA, 0x55555555, 0xFFFFFFFF),
    # XOR
    ("XOR", 0xDEADBEEF, 0xDEADBEEF, 0),
    ("XOR", 0xAAAAAAAA, 0x55555555, 0xFFFFFFFF),
    ("XOR", 0xF0F0F0F0, 0x0FF00FF0, 0xFF00FF00),
    # SLT (com sinal): menor, maior, igual, negativo x positivo, extremos
    ("SLT", 1, 2, 1),
    ("SLT", 2, 1, 0),
    ("SLT", 3, 3, 0),
    ("SLT", -1, 1, 1),
    ("SLT", 1, -1, 0),
    ("SLT", 0x80000000, 0x7FFFFFFF, 1),
    ("SLT", 0x7FFFFFFF, 0x80000000, 0),
    # SLL: 0, 1, limite 31, limite do contrato (32 -> 0), perda de bits
    ("SLL", 1, 0, 1),
    ("SLL", 1, 1, 2),
    ("SLL", 1, 31, 0x80000000),
    ("SLL", 1, 32, 1),
    ("SLL", 0xFFFFFFFF, 4, 0xFFFFFFF0),
    ("SLL", 3, 31, 0x80000000),
    # SRL (lógico): bit mais significativo em 1 não propaga sinal
    ("SRL", 8, 0, 8),
    ("SRL", 8, 1, 4),
    ("SRL", 0x80000000, 1, 0x40000000),
    ("SRL", 0x80000000, 31, 1),
    ("SRL", 0xFFFFFFFF, 4, 0x0FFFFFFF),
    ("SRL", 0x80000000, 32, 0x80000000),
]


@pytest.mark.parametrize("op,a,b,esperado", CASOS)
def test_operacoes_da_alu(op, a, b, esperado):
    assert execute(op, a, b) == esperado


def test_todas_as_operacoes_do_contrato_estao_cobertas():
    from minirv.alu import OPERACOES
    assert {c[0] for c in CASOS} == set(OPERACOES)


def test_entradas_sao_normalizadas_para_32_bits():
    assert execute("ADD", 1 << 32, 1) == 1
    assert execute("SUB", 0, -1) == 1


def test_resultado_sempre_em_32_bits():
    for op in ("ADD", "SUB", "SLL"):
        assert 0 <= execute(op, 0xFFFFFFFF, 0xFFFFFFFF) <= 0xFFFFFFFF


def test_alu_e_combinacional():
    assert [execute("SLT", -1, 1) for _ in range(3)] == [1, 1, 1]


@pytest.mark.parametrize("op", ["MUL", "add", "", None, 1])
def test_operacao_invalida(op):
    with pytest.raises(ValueError, match="desconhecida"):
        execute(op, 1, 2)


@pytest.mark.parametrize("a,b", [(1.5, 1), (1, "2"), (None, 1), (True, 1)])
def test_operando_nao_inteiro(a, b):
    with pytest.raises(ValueError, match="inteiro"):
        execute("ADD", a, b)
