"""Confere o programa preliminar (Semana 07) contra o contrato: mnemônicos, operandos, faixas e rótulos.

Não é um montador: não codifica nada. Só verifica que cada linha seria aceitável segundo o contrato
e que o programa cobre as cinco necessidades (leitura, decisão, estado, escrita e laço).
"""
import re
from pathlib import Path

from minirv.isa import SPEC

ARQ = Path(__file__).resolve().parent.parent / "docs/semanas/Semana-07/controlador-preliminar.s"
REG = re.compile(r"^x([0-9]|[12][0-9]|3[01])$")
NUM = re.compile(r"^-?(0x[0-9A-Fa-f]+|\d+)$")
MEM = re.compile(r"^(-?(?:0x[0-9A-Fa-f]+|\d+))\((x\d+)\)$")


def linhas_de_codigo():
    rotulos, instrucoes = {}, []
    for bruta in ARQ.read_text(encoding="utf-8").splitlines():
        l = bruta.split("#", 1)[0].strip()
        if not l:
            continue
        m = re.match(r"^([A-Za-z_]\w*):\s*(.*)$", l)
        if m:
            assert m.group(1) not in rotulos, f"rótulo duplicado {m.group(1)}"
            rotulos[m.group(1)] = len(instrucoes)
            l = m.group(2)
            if not l:
                continue
        instrucoes.append(l)
    return rotulos, instrucoes


def _separa(l):
    mnem, _, resto = l.partition(" ")
    return mnem.upper(), [o.strip() for o in resto.split(",")]


def test_cada_linha_obedece_ao_contrato():
    rotulos, instrucoes = linhas_de_codigo()
    assert len(instrucoes) > 15
    for l in instrucoes:
        mnem, ops = _separa(l)
        assert mnem in SPEC, f"{mnem} fora do subconjunto: {l}"
        spec = SPEC[mnem]
        formas = [t.strip() for t in spec.syntax.partition(" ")[2].split(",")]
        assert len(ops) == len(formas), l
        for op, forma in zip(ops, formas):
            if forma in ("rd", "rs1", "rs2"):
                assert REG.match(op), f"registrador inválido '{op}' em: {l}"
            elif forma == "imm(rs1)":
                m = MEM.match(op)
                assert m and REG.match(m.group(2)), f"operando de memória inválido '{op}' em: {l}"
                assert spec.imm_min <= int(m.group(1), 0) <= spec.imm_max, l
            else:  # imm, ou rótulo em B/J
                if NUM.match(op):
                    v = int(op, 0)
                    assert spec.imm_min <= v <= spec.imm_max and v % spec.imm_align == 0, l
                else:
                    assert spec.format in ("B", "J") and op in rotulos, f"rótulo indefinido '{op}' em: {l}"


def test_deslocamentos_dos_rotulos_cabem_no_contrato():
    rotulos, instrucoes = linhas_de_codigo()
    for i, l in enumerate(instrucoes):
        mnem, ops = _separa(l)
        if SPEC[mnem].format in ("B", "J") and ops[-1] in rotulos:
            off = (rotulos[ops[-1]] - i) * 4
            s = SPEC[mnem]
            assert s.imm_min <= off <= s.imm_max and off % s.imm_align == 0, (l, off)


def test_cobre_as_cinco_necessidades():
    _, instrucoes = linhas_de_codigo()
    mn = [_separa(l)[0] for l in instrucoes]
    assert "LUI" in mn and "LW" in mn                       # leitura (base + carga)
    assert {"SLT", "BLT"} & set(mn)                         # decisão por limites
    assert {"ADDI", "XOR"} & set(mn)                        # estado (operações R/ADDI)
    assert mn.count("SW") >= 2                              # escrita de atuador e alarme
    assert {"BLT", "BEQ", "BNE", "JAL"} & set(mn)           # laço
    # laço: existe desvio para trás
    rotulos, ins = linhas_de_codigo()
    voltas = [i for i, l in enumerate(ins) if _separa(l)[1][-1] in rotulos and rotulos[_separa(l)[1][-1]] <= i]
    assert voltas, "nenhum desvio para trás (laço)"


def test_base_da_es_e_montada_com_lui():
    rotulos, instrucoes = linhas_de_codigo()
    assert _separa(instrucoes[0]) == ("LUI", ["x10", "0xFFFF0"])
