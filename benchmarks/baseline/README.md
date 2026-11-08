# Linha de base de desempenho (Semana 02)

## Como reproduzir

```bash
python scripts/measure_baseline.py
```

O comando lê `entrada-temperaturas.csv` (gerado de forma determinística se não existir),
executa o benchmark **3 vezes** e grava:

| Arquivo | Conteúdo |
| --- | --- |
| `config.json` | comando, entrada, repetições, premissas do modelo (CPI, clock) e orçamento |
| `entrada-temperaturas.csv` | 1.000 temperaturas inteiras (°C), entre 15 e 35, determinísticas |
| `resultados-brutos.json` | uma entrada por repetição (tempo, memória de pico, rastro, métricas da arquitetura) |
| `ambiente.json` | sistema, versão do Python e processador **onde a medição foi feita** |

## Benchmark

Para cada amostra: `ADDI x1, x0, <temp>` (carrega) e `ADD x2, x2, x1` (acumula).
Com 1.000 amostras: 2.000 instruções; ao final `x2` = soma das temperaturas.
É um esqueleto da carga de controle, suficiente para medir o simulador antes de existir o RV32I completo.

## Atenção

Os valores versionados foram medidos no ambiente descrito em `ambiente.json`
(contêiner Linux de desenvolvimento), **não** na máquina da dupla. Reexecutem o comando
na máquina de vocês antes da avaliação e versionem o novo `resultados-brutos.json`.
