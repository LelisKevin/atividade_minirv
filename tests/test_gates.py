import pytest

from minirv.combinacional.gates import AND, NOT, OR, XOR, bit, xor_sop

TABELA = [  # A, B, AND, OR, XOR
    (0, 0, 0, 0, 0),
    (0, 1, 0, 1, 1),
    (1, 0, 0, 1, 1),
    (1, 1, 1, 1, 0),
]


@pytest.mark.parametrize("a,b,e_and,e_or,e_xor", TABELA)
def test_tabela_verdade(a, b, e_and, e_or, e_xor):
    assert AND(a, b) == e_and
    assert OR(a, b) == e_or
    assert XOR(a, b) == e_xor


def test_not():
    assert NOT(0) == 1
    assert NOT(1) == 0


@pytest.mark.parametrize("a,b,e_and,e_or,e_xor", TABELA)
def test_xor_por_soma_de_produtos_equivale_ao_xor(a, b, e_and, e_or, e_xor):
    assert xor_sop(a, b) == e_xor


@pytest.mark.parametrize("invalido", [2, -1, None, "0", 1.0, True, False])
def test_entrada_invalida_gera_erro(invalido):
    with pytest.raises(ValueError, match="0 ou 1"):
        bit(invalido)
    with pytest.raises(ValueError):
        NOT(invalido)
    with pytest.raises(ValueError):
        AND(invalido, 1)
    with pytest.raises(ValueError):
        OR(0, invalido)
    with pytest.raises(ValueError):
        XOR(invalido, invalido)


def test_tabelas_do_documento_coincidem_com_o_codigo():
    """A tabela documentada é a especificação: lê docs/logica/tabelas-verdade.md e compara."""
    from pathlib import Path
    texto = (Path(__file__).resolve().parent.parent / "docs/logica/tabelas-verdade.md").read_text(encoding="utf-8")
    linhas = [l for l in texto.splitlines() if l.startswith("| ") and l.split("|")[1].strip() in ("0", "1")
              and len(l.split("|")) == 7]  # | A | B | AND | OR | XOR |
    assert len(linhas) == 4
    for l in linhas:
        a, b, e_and, e_or, e_xor = (int(c.strip()) for c in l.strip("|").split("|"))
        assert (AND(a, b), OR(a, b), XOR(a, b)) == (e_and, e_or, e_xor)
