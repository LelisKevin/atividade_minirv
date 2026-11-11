# reatometro_app.py - Interface Principal para a Feira de Projetos
import random
import threading
import time
from pathlib import Path

from minirv.cpu import CPU, load_hex
from minirv.data_memory import DataMemory, IO_CYCLES, IO_INPUT, IO_SIGNAL

PROGRAMA = Path(__file__).resolve().parent.parent / "programs" / "reatometro.hex"
TEMPO_MAXIMO_CPU = 5


def _executar_cpu(cpu, memoria, parar, erros):
    try:
        while not parar.is_set():
            if cpu.step() is None or memoria.read_word(IO_CYCLES) != 0:
                return
    except Exception as erro:
        erros.append(erro)
        parar.set()


def rodar_reatometro():
    programa = load_hex(PROGRAMA)
    ranking = [] # Armazena os resultados da feira: (nome, ciclos, tempo_ms)

    while True:
        print("\n" + "="*55)
        print(" ⚡ REATOMETRO RISC-V — DESAFIO DE REAÇÃO ⚡")
        print("  Simulador MiniRV | Arquitetura de Computadores FAEX")
        print("="*55)
        
        nome = input("\n👉 Digite o nome do participante (ou 'sair' para fechar): ").strip()
        if nome.lower() == 'sair':
            break

        mem = DataMemory()
        cpu = CPU(programa, memory=mem, trace_enabled=False)
        parar = threading.Event()
        erros = []
        worker = threading.Thread(target=_executar_cpu, args=(cpu, mem, parar, erros), daemon=True)

        print("\n🔴 SINAL VERMELHO: Prepare-se... (Aguarde o verde!)")
        worker.start()
        try:
            time.sleep(random.uniform(2.0, 5.0))
            print("\n🟢 SINAL VERDE! PRESSIONE [ENTER] O MAIS RÁPIDO POSSÍVEL!", flush=True)
            t_inicio = time.perf_counter()
            ciclos_inicio = cpu.write_memory_word(IO_SIGNAL, 1)
            input()
            ciclos_fim = cpu.write_memory_word(IO_INPUT, 1)
            t_fim = time.perf_counter()
            worker.join(TEMPO_MAXIMO_CPU)
            if worker.is_alive():
                raise RuntimeError("CPU não concluiu o programa do reatômetro dentro do limite")
            if erros:
                raise RuntimeError("falha durante a execução da CPU do reatômetro") from erros[0]
            if mem.read_word(IO_CYCLES) == 0:
                raise RuntimeError("o programa Assembly não publicou a contagem no registrador MMIO")
        finally:
            parar.set()
            worker.join(1)

        ciclos_riscv = ciclos_fim - ciclos_inicio
        mem.write_word(IO_CYCLES, ciclos_riscv)
        tempo_ms = (t_fim - t_inicio) * 1000

        print("\n" + "-"*45)
        print(f"📊 RESULTADO DE {nome.upper()}:")
        print(f" ⏱️  Tempo de Reação Real: {tempo_ms:.2f} ms")
        print(f" 🔄 Ciclos simulados (uma instrução por ciclo): {ciclos_riscv}")
        print(f" 💻 Iterações do laço Assembly (x3): {cpu.regs.read(3)}")
        print(f" 🧮 Registradores: x1={cpu.regs.read(1)} x3={cpu.regs.read(3)} "
              f"x10=0x{cpu.regs.read(10):08X} x11=0x{cpu.regs.read(11):08X} "
              f"x12=0x{cpu.regs.read(12):08X}")
        print(f" 📈 Instruções executadas na rodada: {cpu.instruction_count}")
        print(f" 📍 Estado Final do PC: 0x{cpu.pc:08X}")
        print("-"*45)

        # Atualiza o Ranking
        ranking.append((nome, ciclos_riscv, tempo_ms))
        ranking.sort(key=lambda x: x[1]) # Ordena pelo menor numero de ciclos

        print("\n🏆 RANKING DOS MAIS RÁPIDOS DA FEIRA 🏆")
        print("-"*55)
        print(f"{'Pos.':<6}{'Nome':<20}{'Ciclos CPU':<15}{'Tempo (ms)':<10}")
        print("-"*55)
        for pos, (p_nome, p_ciclos, p_ms) in enumerate(ranking[:10], start=1):
            print(f"{pos:<6}{p_nome:<20}{p_ciclos:<15}{p_ms:.1f} ms")
        print("-"*55)

if __name__ == "__main__":
    rodar_reatometro()
