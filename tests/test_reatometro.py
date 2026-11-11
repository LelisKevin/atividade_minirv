import re
from pathlib import Path

from minirv import reatometro_app
from minirv.cpu import CPU, load_hex
from minirv.data_memory import DataMemory, IO_CYCLES, IO_INPUT, IO_SIGNAL
from minirv.reatometro_app import PROGRAMA


def test_programa_reatometro_detecta_mmio_e_grava_contador_assembly():
    cpu = CPU(load_hex(PROGRAMA), memory=DataMemory(), trace_enabled=False)
    mem = cpu.memory

    for _ in range(5):
        cpu.step()
    assert cpu.pc == 12

    inicio_medicao = cpu.instruction_count
    mem.write_word(IO_SIGNAL, 1)
    for _ in range(5):
        cpu.step()
    assert cpu.pc == 32
    assert cpu.regs.read(3) == 1

    mem.write_word(IO_INPUT, 1)
    for _ in range(10):
        cpu.step()
        if mem.read_word(IO_CYCLES) != 0:
            break

    assert cpu.pc == 40
    assert mem.read_word(IO_CYCLES) == 2
    assert cpu.instruction_count - inicio_medicao == 10


def test_arquivo_reatometro_e_hex_executavel():
    palavras = load_hex(PROGRAMA)
    assert len(palavras) == 11
    assert Path(PROGRAMA).name == "reatometro.hex"
    cpu = CPU(palavras, memory=DataMemory(), trace_enabled=False)
    assert cpu.step()["instruction"] == "LUI x10, 0x80000"


def test_cpu_reset_reinicia_execucao_mas_preserva_memoria():
    mem = DataMemory()
    cpu = CPU(load_hex(PROGRAMA), memory=mem, trace_enabled=False)
    cpu.step()
    mem.write_word(IO_INPUT, 1)

    cpu.reset()

    assert cpu.pc == 0
    assert cpu.regs.read(10) == 0
    assert cpu.instruction_count == 0
    assert not cpu.halted
    assert mem.read_word(IO_INPUT) == 1


def test_aplicativo_executa_uma_rodada_sem_entrada_interativa(monkeypatch, capsys):
    import time

    sleep_real = time.sleep
    respostas = iter(("Participante", "", "sair"))

    def entrada(_prompt=""):
        resposta = next(respostas)
        if resposta == "":
            sleep_real(0.05)
        return resposta

    monkeypatch.setattr("builtins.input", entrada)
    monkeypatch.setattr(reatometro_app.random, "uniform", lambda _inicio, _fim: 0)
    monkeypatch.setattr(reatometro_app.time, "sleep", lambda _segundos: sleep_real(0.01))

    reatometro_app.rodar_reatometro()

    saida = capsys.readouterr().out
    assert re.search(r"Ciclos simulados \(uma instrução por ciclo\): [1-9]\d*", saida)
    assert "RANKING" in saida
    assert "x10=0x80000000" in saida
    assert "Instruções executadas na rodada:" in saida
