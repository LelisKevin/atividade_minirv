# GitHub, Semana 03: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s03` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-03-word32`
- **Tag ao final:** `s03`
- **Arquivos adicionados:** 6 · **modificados:** 8

## Arquivos adicionados

- `docs/adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md`
- `docs/semanas/Semana-03/relatorio-semana-03.md`
- `evidencias/README.md`
- `minirv/word32.py`
- `tests/test_word32.py`
- `workloads/control/README.md`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `README.md`
- `docs/matriz-requisitos.md`
- `minirv/alu.py`
- `minirv/cpu.py`
- `minirv/decoder.py`
- `minirv/registers.py`
- `minirv/trace.py`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-03-word32

# (3) Commit 1
git add minirv/alu.py minirv/cpu.py minirv/decoder.py minirv/registers.py minirv/trace.py minirv/word32.py tests/test_word32.py
git commit -m "Semana 03: implementa word32 e reaproveita nos módulos existentes"

# (4) Commit 2
git add README.md docs/adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md docs/semanas/Semana-03/relatorio-semana-03.md evidencias/README.md workloads/control/README.md
git commit -m "docs(s03): relatório, ADR-001 e pastas workloads/evidencias"

# (5) Commit 3
git add PROJECT_PROGRESS.md docs/matriz-requisitos.md
git commit -m "docs(s03): atualiza matriz de requisitos e progresso"

# (6) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (7) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-03-word32
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (8) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s03 -m "Semana 03: word32"
git show s03 --stat
git push origin s03
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-03-word32
# copie o conteúdo de Semana_03/ por cima do seu clone (exceto README_SEMANA_03.md e GITHUB_SEMANA_03.md)
git add .
git commit -m "docs(s03): atualiza matriz de requisitos e progresso"
git push -u origin entrega/semana-03-word32
```
