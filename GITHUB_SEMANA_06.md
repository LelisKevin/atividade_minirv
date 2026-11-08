# GitHub, Semana 06: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s06` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-06-ciclo-instrucao`
- **Tag ao final:** `s06`
- **Arquivos adicionados:** 12 · **modificados:** 3

## Arquivos adicionados

- `docs/semanas/Semana-06/diagrama-ciclo.md`
- `docs/semanas/Semana-06/interfaces-barramento.md`
- `docs/semanas/Semana-06/relatorio-semana-06.md`
- `docs/semanas/Semana-06/trace-projeto.json`
- `docs/semanas/Semana-06/verificacao-manual.md`
- `minirv/data_memory.py`
- `minirv/executor.py`
- `minirv/instruction_memory.py`
- `minirv/memory_access.py`
- `tests/test_data_memory.py`
- `tests/test_executor.py`
- `tests/test_instruction_memory.py`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `docs/matriz-requisitos.md`
- `minirv/cpu.py`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-06-ciclo-instrucao

# (3) Commit 1
git add minirv/cpu.py minirv/data_memory.py minirv/executor.py minirv/instruction_memory.py minirv/memory_access.py tests/test_data_memory.py tests/test_executor.py tests/test_instruction_memory.py
git commit -m "Semana 06: memórias de instruções/dados e executor do ciclo de instrução"

# (4) Commit 2
git add docs/semanas/Semana-06/diagrama-ciclo.md docs/semanas/Semana-06/interfaces-barramento.md docs/semanas/Semana-06/relatorio-semana-06.md docs/semanas/Semana-06/trace-projeto.json docs/semanas/Semana-06/verificacao-manual.md
git commit -m "docs(s06): verificação manual, interfaces, diagrama, rastro e relatório"

# (5) Commit 3
git add PROJECT_PROGRESS.md docs/matriz-requisitos.md
git commit -m "docs(s06): atualiza matriz de requisitos e progresso"

# (6) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (7) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-06-ciclo-instrucao
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (8) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s06 -m "Semana 06: ciclo de instrução e interconexões"
git show s06 --stat
git push origin s06
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-06-ciclo-instrucao
# copie o conteúdo de Semana_06/ por cima do seu clone (exceto README_SEMANA_06.md e GITHUB_SEMANA_06.md)
git add .
git commit -m "docs(s06): atualiza matriz de requisitos e progresso"
git push -u origin entrega/semana-06-ciclo-instrucao
```
