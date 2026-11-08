# GitHub, Semana 08: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s08` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-08-consolidacao`
- **Tag ao final:** `s08`
- **Arquivos adicionados:** 3 · **modificados:** 5

## Arquivos adicionados

- `benchmarks/baseline/comparacao-s06-s08.json`
- `docs/checklist-final.md`
- `docs/entrega-github.md`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `README.md`
- `docs/arquitetura.md`
- `docs/matriz-requisitos.md`
- `docs/semanas/Semana-02/orcamento-de-desempenho.md`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-08-consolidacao

# (3) Commit 1
git add PROJECT_PROGRESS.md README.md benchmarks/baseline/comparacao-s06-s08.json docs/arquitetura.md docs/checklist-final.md docs/entrega-github.md docs/matriz-requisitos.md docs/semanas/Semana-02/orcamento-de-desempenho.md
git commit -m "docs(s08): README final, checklist, guia de publicação e atualização do orçamento de desempenho"

# (4) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (5) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-08-consolidacao
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (6) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s08 -m "Semana 08: consolidação"
git show s08 --stat
git push origin s08
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-08-consolidacao
# copie o conteúdo de Semana_08/ por cima do seu clone (exceto README_SEMANA_08.md e GITHUB_SEMANA_08.md)
git add .
git commit -m "docs(s08): README final, checklist, guia de publicação e atualização do orçamento de desempenho"
git push -u origin entrega/semana-08-consolidacao
```
