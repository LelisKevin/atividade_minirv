# Checklist final de entrega

## 1. Resultado dos testes

| Ambiente | Resultado |
| --- | --- |
| Repositório de desenvolvimento (com capstone) | **574 aprovados** |
| Clone limpo, venv novo, só `pytest` instalado | **531 aprovados, 1 ignorado** (o teste opcional do capstone) |

Evolução da suíte: 26 (S1) → 33 (S2) → 60 (S3) → 112 (S4) → 204 (S5) → 251 (S6) → 574 (S7); nenhuma semana quebrou as anteriores.

## 2. Situação dos 70 requisitos (detalhe em `docs/matriz-requisitos.md`)

| Status | Quantidade |
| --- | --- |
| Implementado | 22 |
| Pendente — ação sua | 13 |
| Pendente — decisão sua | 1 |
| Testado e aprovado | 34 |

## 3. O que depende de VOCÊS (não pode ser feito dentro do código)

| ID | Sem. | Requisito | Situação |
| --- | --- | --- | --- |
| R01 | 1 | Repositório GitHub privado, compartilhado com a professora | Exige GitHub/colega/professora |
| R04 | 1 | Issue S01 'Criar núcleo mínimo e primeiro programa' | Exige GitHub/colega/professora |
| R11 | 1 | PR revisada pelo colega e tag s01 | Exige GitHub/colega/professora |
| R16 | 2 | Issue, branch, PR revisada e tag s02 | Issue, PR revisada e tag s02 no GitHub |
| R22 | 3 | Branch, commit, PR revisada e tag s03 | PR revisada e tag s03 no GitHub |
| R31 | 4 | PR revisada e tag s04 | PR revisada e tag s04 no GitHub (só após merge de verdade) |
| R32 | 5 | simulacao-sequencial.md: ≥5 experimentos com previsão e resultado no simulador | Previsões e resultados do projeto preenchidos; resultados do simulador web precisam ser executados e preenchidos por você |
| R40 | 5 | PR revisada e tag s05 | PR revisada e tag s05 no GitHub |
| R41 | 6 | Laboratório da Semana 06 executado e trace-laboratorio salvo | Laboratório web da Semana 06 e exportação do trace-laboratorio.json |
| R52 | 6 | PR revisada e tag s06 | PR revisada e tag s06 no GitHub |
| R53 | 7 | Simulador da Semana 07 executado e vetores exportados | Executar o simulador web e salvar vetores-simulador.json (não foi inventado) |
| R64 | 7 | Contrato v1 declarado congelado após revisão + modelo de ADR | ADR-TEMPLATE criado; contrato está 'candidato a congelamento' até a PR ser revisada |
| R65 | 7 | Suíte completa sem regressões, PR revisada e tag s07 | PR revisada e tag s07 no GitHub |
| R66 | 8 | LACUNA: documento da Semana 8 não fornecido (a Semana 07 prevê montador + execução de Assembly) | Nenhum documento da Semana 8 foi fornecido (7 arquivos, não 8). A Semana 07 prevê montador completo e execução de Assembly; não implementei sem o roteiro. |

Itens de preenchimento humano dentro dos arquivos: nomes dos integrantes, revisor e data nos relatórios; seção 10 do
relatório da Semana 02; comando que funcionou no README; resultados do simulador web na `simulacao-sequencial.md`.

## 4. Lacunas e decisões abertas

1. **Documento da Semana 8 ausente.** Foram enviados 7 arquivos (Semanas 1 a 7 e o Laboratório 03), não 8. A Semana 07 diz que
   o montador completo e a execução de programas Assembly ficam para a Semana 08. Nada disso foi implementado, porque
   o roteiro não existe e a instrução era não inventar requisitos. Com o documento, o contrato (`rv32i-subset-v1.md`, seção 4)
   já define a sintaxe e as mensagens de erro que o montador deve seguir.
2. **ADR-001** (pasta `minirv/` em vez de `src/`, organização da memória) está **Proposto**: a dupla precisa confirmar.
3. **Contrato v1** está "candidato a congelamento": trocar para `CONGELADA` após a revisão da PR (guia, Passo 12).
4. **Regressão de desempenho** de +42% do decodificador novo, justificada na seção 12 de `orcamento-de-desempenho.md`.
5. **Contradições entre os roteiros** (resolvidas no ADR-001 ou no relatório de cada semana): `src/` × `minirv/`; nome
   do repositório (`minirv-dupla-01` × `ac-riscv-2026-dupla-N`); a Semana 01 usa `ecall`, que não está nas 19 instruções;
   a Semana 06 cita uma decisão de memória da Semana 01 que não está registrada lá.

## 5. Estrutura final

```

```
(contagem de arquivos versionados por pasta)

## 6. Histórico

Branches por semana (`feature/s01-nucleo-minimo`, `entrega/semana-02-desempenho` ... `entrega/semana-08-consolidacao`),
commits pequenos com mensagens por semana e merges `--no-ff`. As tags `s01` a `s07` existem **apenas localmente**
(marcam os merges locais). No GitHub elas devem ser criadas só depois da PR revisada.
