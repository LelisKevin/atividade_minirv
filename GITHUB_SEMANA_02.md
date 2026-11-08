# GitHub, Semana 02: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s02` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-02-desempenho`
- **Tag ao final:** `s02`
- **Arquivos adicionados:** 9 · **modificados:** 2

## Arquivos adicionados

- `benchmarks/baseline/README.md`
- `benchmarks/baseline/ambiente.json`
- `benchmarks/baseline/config.json`
- `benchmarks/baseline/entrada-temperaturas.csv`
- `benchmarks/baseline/resultados-brutos.json`
- `docs/adr/ADR-002-metricas-e-limites.md`
- `docs/semanas/Semana-02/orcamento-de-desempenho.md`
- `scripts/measure_baseline.py`
- `tests/test_baseline.py`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `docs/matriz-requisitos.md`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-02-desempenho

# (3) Commit 1
git add scripts/measure_baseline.py tests/test_baseline.py
git commit -m "bench(s02): coletor de métricas com orçamento verificável e testes"

# (4) Commit 2
git add benchmarks/baseline/README.md benchmarks/baseline/ambiente.json benchmarks/baseline/config.json benchmarks/baseline/entrada-temperaturas.csv benchmarks/baseline/resultados-brutos.json
git commit -m "bench(s02): linha de base (entrada, config, resultados brutos de 3 execuções)"

# (5) Commit 3
git add PROJECT_PROGRESS.md docs/adr/ADR-002-metricas-e-limites.md docs/matriz-requisitos.md docs/semanas/Semana-02/orcamento-de-desempenho.md
git commit -m "docs(s02): orçamento de desempenho, ADR-002 e progresso"

# (6) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (7) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-02-desempenho
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (8) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s02 -m "Entrega da Semana 02 - desempenho e orçamento de recursos"
git show s02 --stat
git push origin s02
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-02-desempenho
# copie o conteúdo de Semana_02/ por cima do seu clone (exceto README_SEMANA_02.md e GITHUB_SEMANA_02.md)
git add .
git commit -m "docs(s02): orçamento de desempenho, ADR-002 e progresso"
git push -u origin entrega/semana-02-desempenho
```
