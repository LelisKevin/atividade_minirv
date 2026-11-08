"""Coletor de linha de base de desempenho (Semana 02).

Benchmark: para cada amostra de temperatura da entrada, o MiniRV executa
    ADDI x1, x0, <temperatura>   ; carrega a amostra
    ADD  x2, x2, x1              ; acumula
e ao final x2 contém a soma das temperaturas. É um esqueleto da carga de controle.

Métricas em duas camadas (não misturar):
  - arquitetura simulada: instruções, ciclos, CPI, tempo modelado;
  - computador hospedeiro: tempo decorrido, memória de pico, tamanho do rastro, ambiente.

Uso (na raiz do repositório):  python scripts/measure_baseline.py
"""
import csv
import json
import platform
import sys
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from minirv.cpu import CPU  # noqa: E402
from minirv.encoder import encode  # noqa: E402

BASE = ROOT / "benchmarks" / "baseline"


def gerar_entrada(n):
    """Temperaturas inteiras (°C) determinísticas, entre 15 e 35."""
    return [15 + (i * 7 + (i * i) % 11) % 21 for i in range(n)]


def salvar_entrada(path, temperaturas):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["amostra", "temperatura_c"])
        for i, t in enumerate(temperaturas):
            w.writerow([i, t])


def ler_entrada(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [int(row["temperatura_c"]) for row in csv.DictReader(f)]


def montar_programa(temperaturas):
    palavras = []
    for t in temperaturas:
        palavras.append(encode({"mnemonic": "ADDI", "rd": 1, "rs1": 0, "imm": t}))
        palavras.append(encode({"mnemonic": "ADD", "rd": 2, "rs1": 2, "rs2": 1}))
    return palavras


def executar_benchmark(temperaturas, cpi, clock_hz):
    cpu = CPU(montar_programa(temperaturas))
    instrucoes = cpu.run()
    rastro_bytes = len(cpu.trace.to_json().encode("utf-8"))
    ciclos = instrucoes * cpi
    return {
        "amostras": len(temperaturas),
        "soma_temperaturas": cpu.regs.read(2),
        "tamanho_rastro_bytes": rastro_bytes,
        "arquitetura": {
            "instrucoes_executadas": instrucoes,
            "cpi_modelado": cpi,
            "ciclos_simulados": ciclos,
            "tempo_modelado_s": ciclos / clock_hz,
        },
    }


def executar(config, entrada_path=None, repeticoes=None):
    entrada_path = Path(entrada_path) if entrada_path else ROOT / config["entrada"]
    temperaturas = ler_entrada(entrada_path)
    repeticoes = repeticoes or config["repeticoes"]
    modelo = config["modelo_arquitetural"]
    resultados = []
    for rep in range(1, repeticoes + 1):
        tracemalloc.start()
        inicio = time.perf_counter()
        saida = executar_benchmark(temperaturas, modelo["cpi_modelado"], modelo["clock_modelado_hz"])
        tempo = time.perf_counter() - inicio
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        resultados.append({"repeticao": rep, "tempo_decorrido_s": tempo, "memoria_pico_bytes": pico, **saida})
    return resultados


def ambiente():
    return {
        "sistema": platform.platform(),
        "python": platform.python_version(),
        "implementacao": platform.python_implementation(),
        "processador": platform.processor() or platform.machine(),
        "nota": "Medição feita no ambiente indicado. Reexecute na máquina da dupla para o relatório final.",
    }


def verificar_orcamento(resultados, config):
    """Devolve a lista de violações do orçamento (vazia = dentro do orçamento)."""
    o = config["orcamento"]
    problemas = []
    if len(resultados) < o["repeticoes_minimas"]:
        problemas.append(f"repetições insuficientes: {len(resultados)} < {o['repeticoes_minimas']}")
    media = sum(r["tempo_decorrido_s"] for r in resultados) / len(resultados)
    if media > o["tempo_medio_max_s"]:
        problemas.append(f"tempo médio {media:.3f}s > {o['tempo_medio_max_s']}s")
    if max(r["memoria_pico_bytes"] for r in resultados) > o["memoria_pico_max_bytes"]:
        problemas.append("memória de pico acima do orçamento")
    if max(r["tamanho_rastro_bytes"] for r in resultados) > o["rastro_max_bytes"]:
        problemas.append("rastro acima do orçamento")
    return problemas


def main():
    config = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    entrada = ROOT / config["entrada"]
    if not entrada.exists():
        salvar_entrada(entrada, gerar_entrada(config["amostras"]))
    resultados = executar(config)
    (BASE / "resultados-brutos.json").write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (BASE / "ambiente.json").write_text(
        json.dumps(ambiente(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    problemas = verificar_orcamento(resultados, config)
    for r in resultados:
        print(f"rep {r['repeticao']}: {r['tempo_decorrido_s']*1000:.1f} ms, "
              f"pico {r['memoria_pico_bytes']/1024:.0f} KiB, rastro {r['tamanho_rastro_bytes']/1024:.0f} KiB, "
              f"{r['arquitetura']['instrucoes_executadas']} instruções")
    print("orçamento:", "OK" if not problemas else "; ".join(problemas))
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
