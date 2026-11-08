# GitHub, Semana 05: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s05` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-05-blocos-funcionais`
- **Tag ao final:** `s05`
- **Arquivos adicionados:** 6 · **modificados:** 7

## Arquivos adicionados

- `docs/semanas/Semana-05/mapa-operacoes.md`
- `docs/semanas/Semana-05/relatorio-semana-05.md`
- `docs/semanas/Semana-05/simulacao-sequencial.md`
- `minirv/pc.py`
- `tests/test_pc.py`
- `tests/test_sequencia.py`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `docs/matriz-requisitos.md`
- `minirv/alu.py`
- `minirv/cpu.py`
- `minirv/registers.py`
- `tests/test_alu.py`
- `tests/test_registers.py`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-05-blocos-funcionais

# (3) Commit 1
git add minirv/alu.py minirv/cpu.py minirv/pc.py minirv/registers.py tests/test_alu.py tests/test_pc.py tests/test_registers.py tests/test_sequencia.py
git commit -m "Semana 05: ALU completa, banco de registradores e PC com testes"

# (4) Commit 2
git add docs/semanas/Semana-05/mapa-operacoes.md docs/semanas/Semana-05/relatorio-semana-05.md docs/semanas/Semana-05/simulacao-sequencial.md
git commit -m "docs(s05): mapa de operações, simulação sequencial e relatório"

# (5) Commit 3
git add PROJECT_PROGRESS.md docs/matriz-requisitos.md
git commit -m "docs(s05): atualiza matriz de requisitos e progresso"

# (6) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (7) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-05-blocos-funcionais
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (8) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s05 -m "Semana 05: ALU, registradores e estado sequencial"
git show s05 --stat
git push origin s05
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-05-blocos-funcionais
# copie o conteúdo de Semana_05/ por cima do seu clone (exceto README_SEMANA_05.md e GITHUB_SEMANA_05.md)
git add .
git commit -m "docs(s05): atualiza matriz de requisitos e progresso"
git push -u origin entrega/semana-05-blocos-funcionais
```
