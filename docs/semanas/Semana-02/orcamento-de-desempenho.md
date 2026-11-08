# Semana 02 - Desempenho e orçamento de recursos

## 1. Objetivo e vínculo com o Plano de Aula

Criar uma linha de base de desempenho para o MiniRV: definir como medir, repetir, registrar e
interpretar resultados de forma reprodutível. Não é objetivo otimizar o simulador.
Vínculo: guia do Projeto Integrador, Semana 02 (desempenho e orçamento de recursos).

## 2. Pergunta PBL e hipótese da dupla

**Pergunta:** como saberemos se o simulador e a arquitetura proposta possuem desempenho e uso
de recursos justificáveis?

**Hipótese (proposta para a dupla confirmar ou ajustar):** um benchmark de 1.000 amostras
(2.000 instruções simuladas) executa em bem menos de 2 s, com pico de memória muito abaixo de
150 MB e rastro abaixo de 5 MB. A principal causa de custo esperada é a geração do rastro em
Python (um dicionário por instrução), não a execução da instrução em si.

## 3. Benchmark mínimo definido

- **Entrada:** `benchmarks/baseline/entrada-temperaturas.csv`, 1.000 temperaturas inteiras determinísticas (15 a 35 °C).
- **Programa:** para cada amostra, `ADDI x1, x0, <temp>` e `ADD x2, x2, x1`; ao final `x2` = soma (24715).
- **Comando:** `python scripts/measure_baseline.py`
- **Repetições:** 3, com o mesmo comando.
- **Resultado bruto:** `benchmarks/baseline/resultados-brutos.json` (e `ambiente.json`).
- **Saída mínima exigida:** amostras processadas (1000), tempo decorrido e tamanho do rastro.

## 4. Métricas da arquitetura simulada

Descrevem o **modelo** e não dependem da máquina.

| Métrica | Valor | Observação |
| --- | --- | --- |
| Instruções executadas | 2000 | 2 por amostra |
| CPI modelado | 1.0 | premissa didática (1 ciclo por instrução) |
| Ciclos simulados | 2000 | instruções × CPI |
| Clock modelado | 100 MHz | premissa didática |
| Tempo modelado | 20 µs | ciclos × tempo de ciclo |

CPI, clock e a ausência de *stalls* são **premissas** e não resultados medidos; serão revisadas
quando o ciclo de 5 estados (Semana 06) e o caminho de dados (Semana 09) existirem.

## 5. Métricas do computador hospedeiro

Descrevem a **máquina que executa o simulador** (Linux-6.18.44-fc-v233-x86_64-with-glibc2.39, CPython 3.12.3, x86_64).

- Tempo decorrido real (`time.perf_counter`), média das 3 repetições: **143.1 ms**.
- Memória de pico do processo Python (`tracemalloc`): **4.57 MiB**.
- Tamanho do rastro serializado em JSON: **398 KiB** (407,102 bytes).

> A medição versionada foi feita em contêiner Linux de desenvolvimento, não na máquina da dupla.
> `tracemalloc` mede alocações do Python e não é o mesmo que o RSS do processo.

## 6. Fórmulas e exemplos calculados

| Fórmula | Exemplo calculado |
| --- | --- |
| Tempo de ciclo = 1 / frequência | 1 / 100 MHz = 10 ns |
| CPI = ciclos totais / instruções executadas | 2000 / 2000 = 1,0 |
| Tempo de CPU modelado = instruções × CPI × tempo de ciclo | 2000 × 1,0 × 10 ns = 20 µs |
| Speedup = tempo sequencial / tempo paralelo | 10 s / 4 s = 2,5 |
| Eficiência = speedup / nº de processadores | 2,5 / 4 = 0,625 |
| Lei de Amdahl = 1 / ((1 − f) + f / N) | f = 0,8 e N = 4: 1 / (0,2 + 0,2) = 2,5 |

Exemplo do roteiro: 120.000.000 instruções, CPI 1,5 e 2 GHz → 180.000.000 ciclos e 0,09 s de tempo modelado
(180.000.000 × 0,5 ns).

## 7. Resultados brutos das três execuções

| Rep. | Tempo (ms) | Memória de pico (bytes) | Rastro (bytes) | Instruções | Ciclos | Tempo modelado (µs) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 151.2 | 4.794.244 | 407.102 | 2000 | 2000 | 20.0 |
| 2 | 142.7 | 4.789.236 | 407.102 | 2000 | 2000 | 20.0 |
| 3 | 135.4 | 4.789.228 | 407.102 | 2000 | 2000 | 20.0 |

Média do tempo decorrido: **143.1 ms**. Interpretação: o tempo real é ~7155×
o tempo modelado, o que é esperado, pois o simulador em Python gasta muito mais que o hardware modelado.
Essas duas grandezas não devem ser comparadas como se fossem a mesma.

## 8. Orçamento inicial de recursos

Limite inicial, plausível e revisável (revisões futuras exigem evidência):

| Item | Limite | Medido | Situação |
| --- | --- | --- | --- |
| Repetições obrigatórias | 3 | 3 | dentro |
| Tempo decorrido médio | até 2.0 s | 0.143 s | dentro |
| Memória de pico | até 150 MB | 4.57 MiB | dentro |
| Rastro pequeno | até 5 MB | 0.39 MiB | dentro |
| Regressão relevante | aumento > 10% sem justificativa | n/a (linha de base) | n/a |

A verificação é automatizada por `verificar_orcamento()` no coletor (`python scripts/measure_baseline.py`
retorna código de saída 1 se o orçamento for violado).

## 9. Critérios de aceite: aprovado/pendente + evidência

| Critério | Situação | Evidência |
| --- | --- | --- |
| Benchmark executa com um comando documentado | Aprovado | `python scripts/measure_baseline.py` |
| Resultados brutos de três execuções preservados | Aprovado | `benchmarks/baseline/resultados-brutos.json` |
| Relatório diferencia arquitetura × hospedeiro | Aprovado | seções 4 e 5 |
| Fórmulas com unidades e exemplos | Aprovado | seção 6 |
| Orçamento plausível, mensurável e revisável | Aprovado | seção 8 e `config.json` |
| ADR-002 com contexto, alternativas, decisão, consequências, evidências | Aprovado | `docs/adr/ADR-002-metricas-e-limites.md` |
| Testes do coletor | Aprovado | `tests/test_baseline.py` |
| Issue, branch, PR revisada, merge e tag s02 | **Pendente — ação da dupla** | GitHub |

## 10. Contribuição de cada integrante

_Pendente: a dupla deve preencher quem fez o quê nesta semana e quem revisou a PR._

## 11. Pendências e plano da próxima semana

- Reexecutar o benchmark na máquina da dupla e versionar os novos resultados brutos.
- Semana 03: módulo `word32` (representação de 32 bits), que passa a ser reutilizado por registradores e ULA.
- Quando o RV32I existir (Semana 07), o benchmark deve passar a usar o codificador oficial
  em vez dos dois montadores de palavra locais de `scripts/measure_baseline.py`.

## 12. Atualização da Semana 08: regressão após o decodificador da Semana 07

Regra do orçamento (seção 8): aumento superior a 10% sem justificativa é regressão relevante.

**Medição.** Em 6 repetições por versão, na mesma máquina e no mesmo momento (`benchmarks/baseline/comparacao-s06-s08.json`):
tag `s06` (decodificador antigo) com média de 326,5 ms; `main` (decodificador novo) com média de 463,6 ms, ou seja,
**+42,0%**. A memória de pico ficou praticamente igual (4.678–4.682 KiB contra 4.685 KiB).

**Causa.** O decodificador da Semana 07 deixou de ser um `if` para ADD/ADDI e passou a consultar a especificação do
contrato (19 instruções), extrair o imediato por formato e validar faixa e alinhamento a cada instrução decodificada.
A hipótese inicial de que a montagem do programa com `encode()` fosse a causa foi **medida e descartada**
(≈ 6 ms de ~50 ms sem `tracemalloc`).

**Justificativa e decisão.** A regressão é aceita: o custo extra é o preço de decodificar o subconjunto completo com
validação (requisito da Semana 07), o resultado continua muito abaixo do limite de 2 s e a memória não mudou.
Não foi feita otimização (não é objetivo do projeto).

**Cuidado ao comparar.** Os 135–151 ms da seção 7 foram medidos em outro momento; nessa mesma máquina, hoje, o código
da `s06` leva 280–410 ms. Ou seja, a variação entre momentos (2 a 3 vezes) é maior que a regressão do decodificador.
Compare sempre versões lado a lado e reexecute `python scripts/measure_baseline.py` na máquina da dupla.
