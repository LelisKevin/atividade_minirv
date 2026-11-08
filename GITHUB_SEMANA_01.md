# GitHub, Semana 01: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s01` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `feature/s01-nucleo-minimo`
- **Tag ao final:** `s01`
- **Arquivos adicionados:** 19 · **modificados:** 0

## Arquivos adicionados

- `.gitignore`
- `PROJECT_PROGRESS.md`
- `README.md`
- `docs/arquitetura.md`
- `docs/matriz-requisitos.md`
- `minirv/__init__.py`
- `minirv/alu.py`
- `minirv/cpu.py`
- `minirv/decoder.py`
- `minirv/registers.py`
- `minirv/trace.py`
- `programs/soma.hex`
- `programs/soma.s`
- `pytest.ini`
- `requirements.txt`
- `tests/test_alu.py`
- `tests/test_cpu.py`
- `tests/test_decoder.py`
- `tests/test_registers.py`

## Arquivos modificados

_(nenhum)_

## Ordem correta de execução

```bash
# (1) Criar o repositório PRIVADO no GitHub (sem README) e adicionar a professora. Depois, na pasta do projeto:
git init
git branch -M main
git remote add origin URL_DO_REPOSITORIO   # substitua pela URL do seu repositório

# (2) Criar a branch da semana
# (a primeira alteração fica na main, como no roteiro: 'docs: inicia projeto MiniRV')

# (3) Commit inicial na main
git add .gitignore README.md pytest.ini requirements.txt
git commit -m "docs: inicia projeto MiniRV"
git push -u origin main

# (4) Agora a branch da etapa
git switch -c feature/s01-nucleo-minimo

# (5) Commit 1
git add minirv/__init__.py minirv/alu.py minirv/registers.py tests/test_alu.py tests/test_registers.py
git commit -m "feat(s01): registradores x0-x31 (x0 imutável) e ULA com ADD"

# (6) Commit 2
git add minirv/cpu.py minirv/decoder.py minirv/trace.py programs/soma.hex programs/soma.s tests/test_cpu.py tests/test_decoder.py
git commit -m "feat(s01): decodificador ADD/ADDI, CPU mínima, trace JSON e programa soma"

# (7) Commit 3
git add PROJECT_PROGRESS.md docs/arquitetura.md docs/matriz-requisitos.md
git commit -m "docs(s01): diagrama de arquitetura, matriz de requisitos e progresso"

# (8) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (9) Enviar a branch e abrir a Pull Request
git push -u origin feature/s01-nucleo-minimo
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (10) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s01 -m "Semana 01: núcleo mínimo e primeiro programa"
git show s01 --stat
git push origin s01
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c feature/s01-nucleo-minimo
# copie o conteúdo de Semana_01/ por cima do seu clone (exceto README_SEMANA_01.md e GITHUB_SEMANA_01.md)
git add .
git commit -m "Semana 01: núcleo mínimo e primeiro programa"
git push -u origin feature/s01-nucleo-minimo
```
