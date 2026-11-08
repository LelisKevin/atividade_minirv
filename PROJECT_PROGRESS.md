# Progresso do projeto MiniRV

Registro do andamento real. Nada aqui é marcado como concluído sem ter sido executado.
Matriz completa: [`docs/matriz-requisitos.md`](docs/matriz-requisitos.md).

Legenda: **Testado e aprovado** · **Implementado** (sem teste automatizável) · **Pendente — ação sua**.

## Semana 1 — Estruturação (branch `feature/s01-nucleo-minimo`)

- Testado e aprovado: banco de registradores com x0 imutável, ULA (ADD), decodificador (ADD/ADDI), CPU mínima passo a passo/contínua, trace JSON, programa `soma.hex` (x3 = 12). 26 testes, 26 aprovados.
- Implementado: README, diagrama de arquitetura (Mermaid), `.gitignore`, `requirements.txt`, `pytest.ini`.
- Pendente — ação sua: criar repositório privado e adicionar a professora; abrir a Issue S01; PR revisada pelo colega; tag `s01` no GitHub; preencher nomes no README.
- Observação: o programa do guia usa `addi a7` + `ecall` para sair; `ecall` não pertence ao subconjunto, então `soma.hex` tem só as 3 instruções e a CPU encerra quando o PC passa do fim. O `.s` completo fica em `programs/soma.s` para o RARS.

## Semana 2 — Desempenho e orçamento (branch `entrega/semana-02-desempenho`)

- Testado e aprovado: coletor `scripts/measure_baseline.py` (3 repetições, tempo, memória de pico, tamanho do rastro, métricas da arquitetura separadas das do hospedeiro, verificação de orçamento). Suíte: 33 testes, 33 aprovados.
- Medido (contêiner Linux, Python 3.12.3): média de 143,1 ms, pico de 4,57 MiB, rastro de 0,39 MiB, 2.000 instruções. Orçamento: dentro dos limites.
- Implementado: `orcamento-de-desempenho.md` (11 seções, números gerados a partir do JSON), `ADR-002`, `benchmarks/baseline/README.md`.
- Pendente — ação sua: seção 10 do relatório (contribuição de cada integrante); reexecutar o benchmark na máquina da dupla e versionar o resultado; Issue, PR revisada e tag `s02` no GitHub.
- Premissas (não são medições): CPI = 1,0 e clock = 100 MHz do modelo.

## Semana 3 — Representação de 32 bits (branch `entrega/semana-03-word32`)

- Testado e aprovado: `minirv/word32.py` (normalizar, unsigned, signed, hex, binário, extensão de sinal, soma com overflow). 60 testes, 60 aprovados (27 novos).
- Modificados: `registers.py`, `alu.py`, `cpu.py`, `decoder.py`, `trace.py` passaram a reutilizar `word32` (sem máscara duplicada). Testes das semanas 1 e 2 seguem passando.
- Implementado: relatório da Semana 03 (tabela de casos-limite gerada pelo módulo), `ADR-001`, pastas `workloads/control/` e `evidencias/`.
- Conflitos entre documentos resolvidos no ADR-001 (status **Proposto**: a dupla confirma): `src/` × `minirv/`, nome do repositório, organização da memória (Semana 06 a cita, mas a Semana 01 não a registra).
- Pendente — ação sua: nomes/data/revisor no relatório; confirmar o ADR-001; PR revisada e tag `s03`.

## Semana 4 — Lógica combinacional (branch `entrega/semana-04-logica-digital`)

- Testado e aprovado: portas AND/OR/NOT/XOR (+ XOR por soma de produtos), MUX 2:1, decoder 2→4, `decode_control` (R, I, LOAD, STORE, BRANCH). 112 testes, 112 aprovados (52 novos). Os testes comparam o código com as tabelas dos `.md`.
- Implementado: `docs/logica/tabelas-verdade.md`, `docs/logica/sinais-controle.md`, relatório da Semana 04, diagrama atualizado (blocos combinacionais em azul).
- Decisão: validação estrita de tipo (`True` e `1.0` são rejeitados); teste do decoder 2→4 chama-se `test_decoder2to4.py` para não colidir com `test_decoder.py`.
- Pendente — ação sua: nomes/revisor no relatório; PR revisada e tag `s04` no GitHub após o merge.

## Semana 5 — ALU, registradores e PC (branch `entrega/semana-05-blocos-funcionais`)

- Testado e aprovado: ALU com ADD/SUB/AND/OR/XOR/SLT/SLL/SRL (normal, limites, negativos, overflow), `RegisterFile` com `read2` e `write(enable)`, `ProgramCounter` (avanço, salto validado, reset), desvios por composição (BEQ/BNE/BLT) e sequência x1=5, x2=7, x3=12. 204 testes, 204 aprovados.
- Modificados: `alu.py`, `registers.py` (ampliados), `cpu.py` (passa a usar `ProgramCounter`).
- Implementado: `mapa-operacoes.md` (gerado executando os componentes), `relatorio-semana-05.md` (invariantes ↔ testes), `simulacao-sequencial.md`.
- Pendente — ação sua: **executar o simulador de flip-flops e preencher a coluna "Resultado no simulador da aula"** (5 experimentos); nomes/revisor; PR revisada e tag `s05`.
- Decisão: deslocamentos SLL/SRL usam só os 5 bits menos significativos de `b` (como no RV32I).

## Semana 6 — Ciclo de instrução e memórias (branch `entrega/semana-06-ciclo-instrucao`)

- Testado e aprovado: memória de instruções, memória de dados (alinhamento, faixa, erro com endereço e causa, sem escrita parcial), executor de 5 estados com `step_stage()`, microssequência CADD/CSTORE/CLOAD (x3=12, mem[0]=12, x4=12, PC=0x0000000C). 251 testes, 251 aprovados (47 novos).
- Modificado: `cpu.py` usa `InstructionMemory`.
- Implementado: `trace-projeto.json` (15 eventos), `verificacao-manual.md`, `interfaces-barramento.md`, `diagrama-ciclo.md` (Mermaid), relatório com comparação manual × automático (coincide).
- Pendente — ação sua: **laboratório web da Semana 06 e `trace-laboratorio.json`**; nomes/revisor; PR revisada e tag `s06`.

## Semana 7 — Contrato RV32I v1 (branch `entrega/semana-07-isa-rv32i`)

- Testado e aprovado: `isa.py` (lê o contrato `.md` como fonte única), `encoder.py`, `decoder.py` generalizado (19 instruções, 6 formatos), 43 vetores válidos + 43 negativos, ida e volta aleatória (200.000 palavras), conferência com o manual RISC-V e com o capstone, programa preliminar conferido contra o contrato. 574 testes, 574 aprovados (323 novos). Teste de mutação: 4 de 4 erros injetados foram detectados.
- Implementado: `docs/isa/rv32i-subset-v1.md` (tabela, 6 layouts, sintaxe, erros, regularidade), `mapeamento-carga-isa.md`, `controlador-preliminar.s` (não executado), `ADR-TEMPLATE.md`, relatório.
- Decisões: offsets de branch/jump múltiplos de 4; SLL/SRL por registrador; E/S em 0xFFFF0000 é premissa da dupla.
- **Contrato em "candidato a congelamento":** só vira "CONGELADA" depois da PR revisada (guia, Passo 12).
- Pendente — ação sua: executar o simulador da Semana 07 e salvar `vetores-simulador.json`; revisão cruzada da PR; congelar o contrato; tag `s07`.
