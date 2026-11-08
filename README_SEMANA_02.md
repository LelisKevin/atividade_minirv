# Semana 02: Desempenho e orçamento de recursos

> Esta pasta é o **estado completo do projeto ao final da Semana 02** (conteúdo exato da tag local `s02`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Criar a linha de base de desempenho: benchmark reproduzível, métricas separadas (arquitetura × hospedeiro), orçamento de recursos e ADR (How To Semana 2).

## 2. O que foi desenvolvido

- Coletor `scripts/measure_baseline.py` (3 repetições, tempo, memória de pico, tamanho do rastro, orçamento verificável).
- Entrada determinística de 1.000 temperaturas, resultados brutos reais, relatório de 11 seções e ADR-002.

## 3. Arquivos criados nesta semana (9)

- `benchmarks/baseline/README.md`: Como reproduzir a linha de base de desempenho e o que cada arquivo contém.
- `benchmarks/baseline/ambiente.json`: Ambiente em que a medição foi feita (sistema, Python, processador).
- `benchmarks/baseline/config.json`: Comando, entrada, repetições, premissas do modelo (CPI, clock) e orçamento de recursos.
- `benchmarks/baseline/entrada-temperaturas.csv`: 1.000 temperaturas determinísticas usadas como entrada do benchmark.
- `benchmarks/baseline/resultados-brutos.json`: Resultados brutos de 3 execuções do benchmark.
- `docs/adr/ADR-002-metricas-e-limites.md`: Decisão: métricas em duas camadas e limites iniciais de desempenho.
- `docs/semanas/Semana-02/orcamento-de-desempenho.md`: Relatório de desempenho e orçamento (11 seções; seção 12 acrescentada na Semana 08).
- `scripts/measure_baseline.py`: Coletor de métricas de desempenho com verificação de orçamento.
- `tests/test_baseline.py`: Testes do coletor de métricas e do orçamento.

## 4. Arquivos modificados nesta semana (2)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 1.
- Medir desempenho (3 repetições) e verificar o orçamento.

## 6. O que ainda NÃO existe neste estágio

Ainda não existe `word32`, lógica combinacional, ALU completa, PC, memórias, executor nem contrato RV32I. O benchmark usa montadores locais de ADDI/ADD.

## 7. Como executar e testar esta versão

```bash
cd Semana_02
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.cpu programs/soma.hex
python scripts/measure_baseline.py
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **33 passed in 0.22s** (medido ao gerar este pacote, executando os testes dentro desta pasta).
Arquivos versionados nesta versão: **28** (9 novos, 2 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_01`. Próxima: `../Semana_03`.
Instruções Git desta etapa: `GITHUB_SEMANA_02.md`.
