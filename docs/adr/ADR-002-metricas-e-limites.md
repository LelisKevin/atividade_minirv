# ADR-002 - Métricas e limites de desempenho

Status: aceita

## Contexto

O simulador precisa de uma forma repetível de medir desempenho e uso de recursos antes de
crescer. Sem isso, não é possível distinguir uma regressão real de variação da máquina, nem
separar o desempenho da arquitetura simulada do desempenho do programa Python que a simula.

## Alternativas

1. **Medir só tempo decorrido.** Simples, mas mistura modelo e hospedeiro e ignora memória e rastro.
2. **Duas camadas de métricas (escolhida).** Arquitetura simulada (instruções, ciclos, CPI, tempo modelado)
   separada do hospedeiro (tempo decorrido, memória de pico, tamanho do rastro, ambiente).
3. **Usar ferramenta externa de profiling.** Mais precisa, mas exige dependências e ambiente que a
   disciplina não fixou; adia o hábito de medir.

## Decisão

- Adotar a alternativa 2, com coletor próprio em `scripts/measure_baseline.py` (biblioteca padrão apenas:
  `time.perf_counter` e `tracemalloc`).
- Benchmark: 1.000 temperaturas determinísticas, 3 repetições com o mesmo comando.
- Premissas do modelo: CPI = 1,0 e clock = 100 MHz (didáticas; ficam em `config.json`).
- Limites iniciais: tempo médio ≤ 2 s; memória de pico ≤ 150 MB; rastro ≤ 5 MB; regressão relevante =
  aumento > 10% sem justificativa.

## Consequências

- Ganhos: resultados reproduzíveis, orçamento verificável por código (`verificar_orcamento`), sem dependências.
- Custos: o rastro em JSON domina o uso de memória e tempo; `tracemalloc` desacelera a execução e mede
  alocações Python, não o RSS do processo.
- Riscos: CPI e clock são premissas, não medições; o tempo modelado só terá significado depois do ciclo
  de 5 estados (Semana 06) e do caminho de dados (Semana 09).
- Limitação: variação entre máquinas; os limites devem ser reavaliados com evidência na máquina da dupla.

## Evidências

- `scripts/measure_baseline.py`, `benchmarks/baseline/` (config, entrada, resultados brutos, ambiente).
- `tests/test_baseline.py` (3 repetições, campos numéricos não negativos, reprodutibilidade, orçamento).
- `docs/semanas/Semana-02/orcamento-de-desempenho.md`.
