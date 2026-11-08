import json
import subprocess
import sys
from pathlib import Path

import pytest

from minirv.executor import ESTADOS, Executor, estado_final, micro_sequencia
from minirv.data_memory import DataMemory
from minirv.instruction_memory import InstructionMemory
from minirv.pc import ProgramCounter
from minirv.registers import RegisterFile

ROOT = Path(__file__).resolve().parent.parent


def test_estado_inicial_obrigatorio():
    ex = micro_sequencia()
    r = ex.regs
    assert (r.read(1), r.read(2), r.read(3), r.read(4)) == (5, 7, 0, 0)
    assert ex.dmem.read_word(0) == 0 and ex.pc.value() == 0


def test_estado_final_esperado():
    ex = micro_sequencia()
    assert ex.run() == 3
    assert estado_final(ex) == {"x3": 12, "memória[0]": 12, "x4": 12, "PC final": "0x0000000C"}
    assert ex.finished and ex.step_stage() is None


def test_cinco_estados_observaveis_por_instrucao():
    ex = micro_sequencia()
    assert [e["stage"] for e in ex.step_instruction()] == list(ESTADOS)
    assert ex.current_stage == "FETCH"


def test_step_stage_avanca_um_estado_por_vez():
    ex = micro_sequencia()
    vistos = []
    for _ in range(5):
        vistos.append(ex.current_stage)
        ex.step_stage()
    assert vistos == list(ESTADOS)
    assert ex.regs.read(3) == 12 and ex.pc.value() == 4  # PC só muda no WRITEBACK


def test_pc_so_muda_no_writeback():
    ex = micro_sequencia()
    for estagio in ESTADOS[:-1]:
        ex.step_stage()
        assert ex.pc.value() == 0, estagio
    ex.step_stage()
    assert ex.pc.value() == 4


def test_memoria_de_dados_so_muda_quando_ha_escrita():
    ex = micro_sequencia()
    ex.step_instruction()                      # I1 (CADD)
    assert ex.dmem.read_word(0) == 0
    ex.step_instruction()                      # I2 (CSTORE)
    assert ex.dmem.read_word(0) == 12
    ex.step_instruction()                      # I3 (CLOAD) não escreve
    assert ex.dmem.read_word(0) == 12


def test_trace_tem_15_eventos_sequenciais_e_campos_obrigatorios():
    ex = micro_sequencia(); ex.run()
    t = ex.trace.records
    assert [e["seq"] for e in t] == list(range(1, 16))
    assert all(set(e) == {"seq", "pc", "word", "stage", "signals", "operands", "change"} for e in t)
    assert [e["stage"] for e in t] == list(ESTADOS) * 3
    assert {e["pc"] for e in t[:5]} == {"0x00000000"} and {e["pc"] for e in t[10:]} == {"0x00000008"}
    json.dumps(t)  # serializável


def test_evento_5_igual_ao_exemplo_do_guia():
    ex = micro_sequencia(); ex.run()
    assert ex.trace.records[4] == {
        "seq": 5, "pc": "0x00000000", "word": "0x01000001", "stage": "WRITEBACK",
        "signals": {"RegWrite": 1}, "operands": {"x1": 5, "x2": 7},
        "change": {"x3": 12, "pc_next": "0x00000004"},
    }


def test_rastro_reconstroi_as_alteracoes_de_estado():
    ex = micro_sequencia(); ex.run()
    mud = [(e["pc"], e["change"]) for e in ex.trace.records if e["change"]]
    assert mud == [
        ("0x00000000", {"x3": 12, "pc_next": "0x00000004"}),
        ("0x00000004", {"mem[0]": 12}),
        ("0x00000004", {"pc_next": "0x00000008"}),
        ("0x00000008", {"x4": 12, "pc_next": "0x0000000C"}),
    ]


def test_sinais_de_controle_por_instrucao():
    ex = micro_sequencia(); ex.run()
    dec = [e["signals"] for e in ex.trace.records if e["stage"] == "DECODE"]
    assert [(d["op"], d["RegWrite"], d["MemRead"], d["MemWrite"]) for d in dec] == [
        ("CADD", 1, 0, 0), ("CSTORE", 0, 0, 1), ("CLOAD", 1, 1, 0)]


def test_palavra_desconhecida_gera_erro_explicito():
    ex = Executor(InstructionMemory([0x04000004]), DataMemory(), RegisterFile(), ProgramCounter())
    ex.step_stage()  # FETCH
    with pytest.raises(ValueError, match="desconhecida.*0x04000004"):
        ex.step_stage()


def test_x0_nao_e_alterado_pelo_ciclo():
    ex = micro_sequencia(); ex.run()
    assert ex.regs.read(0) == 0


def test_linha_de_comando_gera_rastro(tmp_path):
    out = tmp_path / "t.json"
    r = subprocess.run([sys.executable, "-m", "minirv.executor", "--trace", str(out)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert len(json.loads(out.read_text(encoding="utf-8"))) == 15 and "0x0000000C" in r.stdout
