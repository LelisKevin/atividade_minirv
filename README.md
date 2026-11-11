# MiniRV

Simulador didático de uma CPU RISC-V (RV32I reduzida) em Python.
Projeto Integrador de **Arquitetura de Computadores** (ADS, FAEX, 2026), Profa. Denise Ribeiro.

## Problema

Entender, de forma observável, como uma CPU busca, decodifica e executa instruções.
O MiniRV recebe instruções em hexadecimal, busca cada uma pelo PC, decodifica os
campos, executa e atualiza o estado (registradores e PC), registrando um *trace*.

## Objetivo

Construir, semana a semana, um simulador pequeno, testável e rastreável de uma CPU RV32I reduzida.

## Estado atual (Semanas 1 a 7 concluídas no código; ver `PROJECT_PROGRESS.md`)

| Capacidade | Onde |
| --- | --- |
| CPU que executa `ADD`, `ADDI`, `LUI`, `LW`, `SW`, `BEQ` e `JAL` | `minirv/cpu.py` |
| Programa interativo do reatômetro com MMIO | `minirv/reatometro_app.py`, `programs/reatometro.s`, `programs/reatometro.hex` |
| Palavra de 32 bits, ALU (8 operações), 32 registradores (x0 = 0), PC | `word32.py`, `alu.py`, `registers.py`, `pc.py` |
| Lógica combinacional (portas, MUX, decoder 2→4, controle) | `minirv/combinacional/` |
| Memória de instruções e de dados, ciclo FETCH→WRITEBACK com rastro | `instruction_memory.py`, `data_memory.py`, `executor.py` |
| Contrato RV32I v1 (19 instruções), encode/decode e vetores | `docs/isa/rv32i-subset-v1.md`, `isa.py`, `encoder.py`, `decoder.py` |
| Linha de base de desempenho e orçamento | `scripts/measure_baseline.py`, `benchmarks/baseline/` |

**Ainda não existe:** montador de Assembly nem execução completa das 19 instruções RV32I v1. A CPU executa o
subconjunto indicado acima; as demais instruções são decodificadas, mas ainda não executadas.

## Decisões fixadas pela disciplina

| Item | Decisão |
| --- | --- |
| Linguagem | Python 3.11 ou superior |
| Arquitetura | RISC-V RV32I reduzida |
| Registradores | x0-x31; x0 sempre zero |
| Execução | Passo a passo e contínua |
| Versionamento | GitHub privado; dupla + professora |

## Ferramentas

Python 3.11+, Git, VS Code, pytest. RARS (opcional) apenas para conferir o Assembly.

## Como executar

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate   |   Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

pytest -q                                        # roda todos os testes
python -m minirv.cpu programs/soma.hex           # execução contínua (trace JSON no stdout)
python -m minirv.cpu programs/soma.hex --step    # passo a passo (Enter avança)
python -m minirv.cpu programs/soma.hex -o trace.json
python -m minirv.reatometro_app                  # reatômetro interativo com MMIO
python -m minirv.executor --trace trace.json     # ciclo de 5 estados (Semana 06)
python scripts/measure_baseline.py               # linha de base de desempenho (Semana 02)
```

Opcional: `python -m pip install -r requirements-dev.txt` habilita a conferência dos vetores RV32I por um
desassemblador independente (capstone); sem ele esse teste é ignorado.

> No Windows, se `python` não funcionar, use `py`. **Registrem aqui qual comando funcionou
> na máquina de vocês:** `____________`

## Estrutura

```
minirv/        pacote do simulador (word32, registers, alu, pc, memórias, executor, isa, encoder, decoder, cpu, trace)
programs/      programas em hexadecimal (soma.hex) e Assembly de referência (soma.s)
tests/         testes automatizados (pytest)
scripts/       coletor de métricas de desempenho
benchmarks/    linha de base de desempenho (entrada, configuração, resultados brutos)
workloads/     carga de trabalho de controle (ver docs/semanas/Semana-07)
docs/          arquitetura, contrato da ISA, ADRs, matriz de requisitos, checklist e relatórios por semana
evidencias/    evidências externas ao código (exportações dos simuladores, capturas)
```

Decisões de organização (pasta `minirv/` em vez de `src/`, memória): [`docs/adr/ADR-001`](docs/adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md).

Diagrama de blocos: [`docs/arquitetura.md`](docs/arquitetura.md) · Requisitos: [`docs/matriz-requisitos.md`](docs/matriz-requisitos.md) · Entrega: [`docs/checklist-final.md`](docs/checklist-final.md) · Publicação: [`docs/entrega-github.md`](docs/entrega-github.md).

## Divisão de responsabilidades

| Integrante | Responsabilidade nesta semana | Revisor |
| --- | --- | --- |
| _(preencher: nome 1)_ | _(preencher)_ | _(preencher)_ |
| _(preencher: nome 2)_ | _(preencher)_ | _(preencher)_ |

Os papéis alternam ao longo das semanas.
