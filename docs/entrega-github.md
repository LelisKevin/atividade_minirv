# Como publicar no GitHub

O projeto foi desenvolvido num repositório **local**, sem acesso ao GitHub (não há credenciais nem URL no ambiente de
desenvolvimento). Nada foi enviado; os merges e as tags `s01`–`s08` são locais.

O pacote `minirv-dupla-01.bundle` contém **todas as branches** (uma por semana). O guia exige PR revisada pelo colega
antes de cada tag, então o caminho recomendado é a **Opção B**, que gera uma PR por semana no repositório que vocês já usam.

## Opção B (recomendada): uma PR por semana no repositório existente

Pré-requisito: clone do repositório da dupla, com `main` atualizada. Coloque o `.bundle` ao lado da pasta do clone.

```bash
cd minirv-dupla-01                       # seu clone
git switch main && git pull --ff-only origin main
git fetch ../minirv-dupla-01.bundle 'refs/heads/*:refs/remotes/pacote/*'
git branch -r | grep pacote              # confira as 8 branches do pacote
```

Repita para cada semana que ainda não foi entregue (exemplo: Semana 07):

```bash
git switch main
git switch -c entrega/semana-07-isa-rv32i
git checkout pacote/entrega/semana-07-isa-rv32i -- .     # traz os arquivos daquela semana (acumulado)
git status                                               # revise o que mudou
python -m pytest -q                                      # deve passar
git add .
git commit -m "Semana 07: congela contrato do subconjunto RV32I"
git push -u origin entrega/semana-07-isa-rv32i
```

1. Abra a Pull Request no GitHub e peça a **revisão cruzada** ao colega; corrija o que ele apontar.
2. Faça o merge e só então crie a tag:

```bash
git switch main && git pull --ff-only origin main
python -m pytest -q
git tag -a s07 -m "Semana 07: contrato RV32I v1"
git show s07 --stat
git push origin s07
```

Observações:
- `git checkout <ref> -- .` copia e sobrescreve arquivos, mas **não apaga** arquivos que existam só no seu repositório.
- Os commits ficam no nome de vocês. No pacote, a autoria é "Claude (assistente de desenvolvimento)".
- Nomes de branch: Semana 01 `feature/s01-nucleo-minimo`; Semanas 02 a 08 `entrega/semana-NN-...` (listadas por `git branch -r`).
- **Semana 07:** só depois da revisão da PR, troque em `docs/isa/rv32i-subset-v1.md` a linha de status por
  `Status: v1 CONGELADA` e faça o commit antes do merge.

## Opção A: repositório novo e vazio (sem PRs)

```bash
git clone minirv-dupla-01.bundle minirv-dupla-01-novo
cd minirv-dupla-01-novo
git remote set-url origin <URL_DO_NOVO_REPOSITORIO_PRIVADO>
git push -u origin main
git push origin --all          # envia as branches; as tags NÃO são enviadas
```

Como todas as branches já estão integradas na `main`, não haverá diferença para abrir PRs ("there isn't anything to
compare"). Use esta opção só se a prova de PRs semanais não for necessária. **Não envie as tags** (`git push --tags`)
sem a revisão correspondente.

## Depois de publicar

```bash
git ls-remote --tags origin      # confira as tags no GitHub
git log --oneline --graph --decorate -15
```
Adicione a professora ao repositório privado e preencha os itens listados em `docs/checklist-final.md`, seção 3.
