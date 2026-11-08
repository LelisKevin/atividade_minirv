"""Validação INDEPENDENTE: os vetores são desmontados pelo capstone (não usa o código do MiniRV).

Compara mnemônico, registradores e imediatos. Pseudoinstruções do capstone (neg, ret, j, beqz e
'jal alvo') escondem operandos implícitos; nesses casos compara-se só o que ele mostra.
"""
import json
import re
from pathlib import Path

import pytest

capstone = pytest.importorskip("capstone")
from capstone import CS_ARCH_RISCV, CS_MODE_RISCV32, Cs  # noqa: E402

ABI = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1"] + [f"a{i}" for i in range(8)] \
    + [f"s{i}" for i in range(2, 12)] + [f"t{i}" for i in range(3, 7)]
ALIAS = {"neg": "sub", "ret": "jalr", "j": "jal", "beqz": "beq"}
VETORES = json.loads((Path(__file__).parent / "vectors" / "rv32i-v1.json").read_text(encoding="utf-8"))


def _numeros(op_str):
    return [int(t, 0) for t in re.findall(r"-?0x[0-9a-fA-F]+|-?\d+(?![\w])", op_str.replace("(", " ").replace(")", " "))]


@pytest.mark.parametrize("v", VETORES, ids=[v["assembly"] for v in VETORES])
def test_capstone_concorda_com_o_vetor(v):
    md = Cs(CS_ARCH_RISCV, CS_MODE_RISCV32)
    ins = list(md.disasm(int(v["word"], 16).to_bytes(4, "little"), 0))
    assert len(ins) == 1, "capstone não reconheceu a palavra"
    c, e = ins[0], v["expected"]
    assert ALIAS.get(c.mnemonic, c.mnemonic) == e["mnemonic"].lower()

    nomes = [ABI[e[k]] for k in ("rd", "rs1", "rs2") if k in e]
    vistos = [t for t in re.findall(r"[a-z]\w*", c.op_str) if t in ABI]
    if c.mnemonic in ALIAS or (c.mnemonic == "jal" and c.op_str.count(",") == 0):
        assert set(vistos) <= set(nomes)           # alias esconde operandos implícitos
    else:
        assert sorted(vistos) == sorted(nomes)
        # ordem: o capstone imprime rd, rs1, rs2 para R/I/B (STORE imprime rs2 antes de rs1)
        esperada = nomes if e["mnemonic"] not in ("SW", "BEQ", "BNE", "BLT") else \
            ([ABI[e["rs2"]], ABI[e["rs1"]]] if e["mnemonic"] == "SW" else [ABI[e["rs1"]], ABI[e["rs2"]]])
        if e["mnemonic"] in ("LW", "JALR"):
            esperada = [ABI[e["rd"]], ABI[e["rs1"]]]
        assert vistos == esperada
    if "imm" in e and not (e["imm"] == 0 and not _numeros(c.op_str)):
        assert e["imm"] in _numeros(c.op_str)
