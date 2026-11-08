import subprocess
import sys
from pathlib import Path

import pytest

from minirv.cpu import CPU, load_hex

ROOT = Path(__file__).resolve().parent.parent
SOMA = ROOT / "programs" / "soma.hex"


def test_programa_soma_5_mais_7():
    cpu = CPU(load_hex(SOMA))
    assert cpu.run() == 3
    assert (cpu.regs.read(1), cpu.regs.read(2), cpu.regs.read(3)) == (5, 7, 12)
    assert cpu.pc == 0x0000000C


def test_trace_primeira_instrucao_segue_formato_do_guia():
    cpu = CPU(load_hex(SOMA))
    cpu.run()
    assert cpu.trace.records[0] == {
        "pc": "0x00000000",
        "instruction": "ADDI x1, x0, 5",
        "registers_read": {"x0": 0},
        "registers_written": {"x1": 5},
        "next_pc": "0x00000004",
    }
    assert cpu.trace.records[2]["registers_read"] == {"x1": 5, "x2": 7}
    assert cpu.trace.records[2]["registers_written"] == {"x3": 12}


def test_x0_continua_zero_mesmo_com_escrita_em_x0():
    cpu = CPU([0x00500013])  # addi x0, x0, 5
    cpu.run()
    assert cpu.regs.read(0) == 0
    assert cpu.trace.records[0]["registers_written"] == {}


def test_passo_a_passo():
    cpu = CPU(load_hex(SOMA))
    assert cpu.step()["instruction"] == "ADDI x1, x0, 5"
    assert cpu.regs.read(1) == 5 and cpu.regs.read(2) == 0
    cpu.step(); cpu.step()
    assert cpu.step() is None and cpu.halted


def test_instrucao_nao_suportada_nao_passa_em_silencio():
    with pytest.raises(ValueError, match="não suportada"):
        CPU([0x00000073]).run()


def test_load_hex_invalido(tmp_path):
    f = tmp_path / "ruim.hex"
    f.write_text("ZZZZ\n")
    with pytest.raises(ValueError, match="hexadecimal inválido"):
        load_hex(f)


def test_linha_de_comando(tmp_path):
    out = tmp_path / "trace.json"
    r = subprocess.run([sys.executable, "-m", "minirv.cpu", str(SOMA), "-o", str(out)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists() and '"ADD x3, x1, x2"' in out.read_text(encoding="utf-8")
    assert "'x3': 12" in r.stderr


def test_instrucao_decodificada_mas_nao_executada_gera_erro_explicito():
    from minirv.encoder import encode
    with pytest.raises(ValueError, match="ainda não executada pela CPU: SUB"):
        CPU([encode({"mnemonic": "SUB", "rd": 1, "rs1": 2, "rs2": 3})]).run()
