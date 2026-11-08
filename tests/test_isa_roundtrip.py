"""Propriedade principal da Semana 07: encode -> decode preserva mnemônico e campos relevantes."""
import random

import pytest

from minirv.decoder import decode
from minirv.encoder import encode
from minirv.isa import SPEC, ISAError


def instrucao_aleatoria(spec, rng):
    d = {"mnemonic": spec.mnemonic}
    for campo in spec.fields:
        if campo == "imm":
            passos = (spec.imm_max - spec.imm_min) // spec.imm_align
            d["imm"] = spec.imm_min + rng.randint(0, passos) * spec.imm_align
        else:
            d[campo] = rng.randint(0, 31)
    return d


@pytest.mark.parametrize("mnemonico", sorted(SPEC))
def test_ida_e_volta_aleatoria(mnemonico):
    spec, rng = SPEC[mnemonico], random.Random(2026)
    for _ in range(500):
        instr = instrucao_aleatoria(spec, rng)
        word = encode(instr)
        assert 0 <= word <= 0xFFFFFFFF
        decoded = decode(word)
        assert decoded["mnemonic"] == instr["mnemonic"] and decoded["format"] == spec.format
        # só campos relevantes: o decodificado tem exatamente os campos do formato
        assert set(decoded) == {"mnemonic", "format", *spec.fields}
        assert {k: decoded[k] for k in spec.fields} == {k: instr[k] for k in spec.fields}
        assert encode(decoded) == word


@pytest.mark.parametrize("mnemonico", sorted(m for m, s in SPEC.items() if "imm" in s.fields))
def test_limites_do_imediato_ida_e_volta(mnemonico):
    spec = SPEC[mnemonico]
    base = {c: 7 for c in spec.fields if c != "imm"}
    for imm in (spec.imm_min, spec.imm_min + spec.imm_align, 0 if spec.imm_min <= 0 else spec.imm_min,
                spec.imm_max - spec.imm_align, spec.imm_max):
        instr = {"mnemonic": mnemonico, **base, "imm": imm}
        assert decode(encode(instr))["imm"] == imm


@pytest.mark.parametrize("mnemonico", sorted(SPEC))
def test_todos_os_registradores_ida_e_volta(mnemonico):
    spec = SPEC[mnemonico]
    regs = [c for c in spec.fields if c != "imm"]
    for r in range(32):
        instr = {"mnemonic": mnemonico, **{c: r for c in regs}}
        if "imm" in spec.fields:
            instr["imm"] = spec.imm_min if spec.imm_min > 0 else 4 * (spec.imm_min // 4 + 1)
        d = decode(encode(instr))
        assert all(d[c] == r for c in regs)


def test_volta_inversa_para_qualquer_palavra_suportada():
    """Toda palavra que decodifica é recodificada exatamente igual (todos os 32 bits têm significado)."""
    rng = random.Random(7)
    aceitas = 0
    for _ in range(200_000):
        w = rng.getrandbits(32)
        try:
            d = decode(w)
        except ISAError:
            continue
        aceitas += 1
        assert encode(d) == w
    assert aceitas > 1000  # a amostra realmente exercitou o caminho feliz
