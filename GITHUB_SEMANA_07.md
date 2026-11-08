# GitHub, Semana 07: sequência SUGERIDA

> **São sugestões** para reproduzir esta etapa; não há datas nem hashes reais de um repositório remoto.
> As mensagens de commit abaixo são as usadas ao construir este pacote localmente. No repositório local de origem os
> merges e a tag `s07` foram feitos sem revisão de PR; no GitHub, crie a tag **só depois** da PR revisada.

- **Branch recomendada:** `entrega/semana-07-isa-rv32i`
- **Tag ao final:** `s07`
- **Arquivos adicionados:** 16 · **modificados:** 6

## Arquivos adicionados

- `docs/adr/ADR-TEMPLATE.md`
- `docs/isa/rv32i-subset-v1.md`
- `docs/semanas/Semana-07/controlador-preliminar.s`
- `docs/semanas/Semana-07/mapeamento-carga-isa.md`
- `docs/semanas/Semana-07/relatorio-semana-07.md`
- `minirv/encoder.py`
- `minirv/isa.py`
- `requirements-dev.txt`
- `tests/test_controlador_preliminar.py`
- `tests/test_isa_capstone.py`
- `tests/test_isa_contrato.py`
- `tests/test_isa_negativos.py`
- `tests/test_isa_roundtrip.py`
- `tests/test_isa_vetores.py`
- `tests/vectors/rv32i-v1-negativos.json`
- `tests/vectors/rv32i-v1.json`

## Arquivos modificados

- `PROJECT_PROGRESS.md`
- `docs/matriz-requisitos.md`
- `minirv/cpu.py`
- `minirv/decoder.py`
- `scripts/measure_baseline.py`
- `tests/test_cpu.py`

## Ordem correta de execução

```bash
# (1) Partir da main atualizada e conferir que a versão anterior passa nos testes
git switch main
git pull --ff-only origin main
python -m pytest -q

# (2) Criar a branch da semana
git switch -c entrega/semana-07-isa-rv32i

# (3) Commit 1
git add docs/isa/rv32i-subset-v1.md minirv/cpu.py minirv/decoder.py minirv/encoder.py minirv/isa.py scripts/measure_baseline.py
git commit -m "Semana 07: contrato RV32I v1 e encode/decode baseados na mesma especificação"

# (4) Commit 2
git add requirements-dev.txt tests/test_controlador_preliminar.py tests/test_cpu.py tests/test_isa_capstone.py tests/test_isa_contrato.py tests/test_isa_negativos.py tests/test_isa_roundtrip.py tests/test_isa_vetores.py tests/vectors/rv32i-v1-negativos.json tests/vectors/rv32i-v1.json
git commit -m "test(s07): vetores, negativos, ida e volta, contrato, capstone e programa preliminar"

# (5) Commit 3
git add docs/adr/ADR-TEMPLATE.md docs/semanas/Semana-07/controlador-preliminar.s docs/semanas/Semana-07/mapeamento-carga-isa.md docs/semanas/Semana-07/relatorio-semana-07.md
git commit -m "docs(s07): mapeamento da carga, programa preliminar, modelo de ADR e relatório"

# (6) Commit 4
git add PROJECT_PROGRESS.md docs/matriz-requisitos.md
git commit -m "docs(s07): atualiza matriz de requisitos e progresso"

# (7) Conferir e rodar a suíte antes de enviar
git status
python -m pytest -q

# (8) Enviar a branch e abrir a Pull Request
git push -u origin entrega/semana-07-isa-rv32i
# Abra a PR no GitHub, peça a revisão cruzada ao colega e corrija o que for apontado.

# (9) Somente DEPOIS do merge da PR: sincronizar a main e criar a tag
git switch main
git pull --ff-only origin main
python -m pytest -q
git tag -a s07 -m "Semana 07: contrato RV32I v1"
git show s07 --stat
git push origin s07
```

## Alternativa (copiar esta pasta para o seu clone)

Se vocês já têm o repositório e querem aplicar esta etapa copiando arquivos:

```bash
git switch main && git pull --ff-only origin main
git switch -c entrega/semana-07-isa-rv32i
# copie o conteúdo de Semana_07/ por cima do seu clone (exceto README_SEMANA_07.md e GITHUB_SEMANA_07.md)
git add .
git commit -m "docs(s07): atualiza matriz de requisitos e progresso"
git push -u origin entrega/semana-07-isa-rv32i
```
