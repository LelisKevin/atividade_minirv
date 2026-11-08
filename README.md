# MiniRV

Simulador didático de uma CPU RISC-V (RV32I reduzida) em Python.
Projeto Integrador de **Arquitetura de Computadores** (ADS, FAEX, 2026), Profa. Denise Ribeiro.

## Problema

Entender, de forma observável, como uma CPU busca, decodifica e executa instruções.
O MiniRV recebe instruções em hexadecimal, busca cada uma pelo PC, decodifica os
campos, executa e atualiza o estado (registradores e PC), registrando um *trace*.

## Objetivo

Construir, semana a semana, um simulador pequeno, testável e rastreável.
Esta versão (Semana 01) executa `ADDI` e `ADD`, altera registradores e gera trace JSON.

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
```

> No Windows, se `python` não funcionar, use `py`. **Registrem aqui qual comando funcionou
> na máquina de vocês:** `____________`

## Estrutura

```
minirv/        pacote do simulador (word32, registers, alu, decoder, cpu, trace)
programs/      programas em hexadecimal (soma.hex) e Assembly de referência (soma.s)
tests/         testes automatizados (pytest)
scripts/       coletor de métricas de desempenho
benchmarks/    linha de base de desempenho (entrada, configuração, resultados brutos)
workloads/     carga de trabalho de controle (ver docs/semanas/Semana-07)
docs/          documentação: arquitetura, ADRs e relatórios por semana
evidencias/    evidências externas ao código (exportações dos simuladores, capturas)
```

Decisões de organização (pasta `minirv/` em vez de `src/`, memória): [`docs/adr/ADR-001`](docs/adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md).

Diagrama de blocos: [`docs/arquitetura.md`](docs/arquitetura.md).

## Divisão de responsabilidades

| Integrante | Responsabilidade nesta semana | Revisor |
| --- | --- | --- |
| _(preencher: nome 1)_ | _(preencher)_ | _(preencher)_ |
| _(preencher: nome 2)_ | _(preencher)_ | _(preencher)_ |

Os papéis alternam ao longo das semanas.
