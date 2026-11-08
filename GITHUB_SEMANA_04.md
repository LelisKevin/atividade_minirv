# GitHub, Semana 04: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s04` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-04-logica-digital`
- **Tag ao final:** `s04`
- **Arquivos adicionados:** 12 · **modificados:** 3

## Arquivos adicionados

- `docs/logica/sinais-controle.md`
- `docs/logica/tabelas-verdade.md`
- `docs/semanas/Semana-04/relatorio-semana-04.md`
- `minirv/combinacional/__init__.py`
- `minirv/combinacional/control.py`
- `minirv/combinacional/decoder.py`
- `minirv/combinacional/gates.py`
- `minirv/combinacional/mux.py`
- `tests/test_control.py`
- `tests/test_decoder2to4.py`
- `tests/test_gates.py`
- `tests/test_mux.py`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `docs/arquitetura.md`
- `docs/matriz-requisitos.md`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-04-logica-digital

# (3) Commit 1
git add minirv/combinacional/__init__.py minirv/combinacional/control.py minirv/combinacional/decoder.py minirv/combinacional/gates.py minirv/combinacional/mux.py tests/test_control.py tests/test_decoder2to4.py tests/test_gates.py tests/test_mux.py
git commit -m "Semana 04: lógica combinacional, MUX e decoder"

# (4) Commit 2
git add docs/arquitetura.md docs/logica/sinais-controle.md docs/logica/tabelas-verdade.md docs/semanas/Semana-04/relatorio-semana-04.md
git commit -m "docs(s04): tabelas-verdade, sinais de controle, diagrama e relatório"

# (5) Commit 3
git add PROJECT_PROGRESS.md docs/matriz-requisitos.md
git commit -m "docs(s04): atualiza matriz de requisitos e progresso"

# (6) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (7) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-04-logica-digital
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (8) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s04 -m "Semana 04: lógica combinacional"
git show s04 --stat
git push origin s04
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-04-logica-digital
# copie o conteúdo de Semana_04/ por cima do seu clone (exceto README_SEMANA_04.md e GITHUB_SEMANA_04.md)
git add .
git commit -m "docs(s04): atualiza matriz de requisitos e progresso"
git push -u origin entrega/semana-04-logica-digital
```
