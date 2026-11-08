# Matriz de requisitos

Fontes: HT1/HT2 = How To Semanas 1 e 2; LAB3 = Laboratório 03; S4–S7 = Atividades das Semanas 4 a 7.
Status: **Testado e aprovado** (coberto por testes automatizados que passaram) · **Implementado** (documento/config criado e conferido, sem teste automatizado) · **Pendente — ação sua** (depende de GitHub, professora, colega ou simulador da aula) · **Pendente**.

| ID | Sem. | Requisito | Fonte | Entrega | Status | Evidência |
|---|---|---|---|---|---|---|
| R01 | 1 | Repositório GitHub privado, compartilhado com a professora | HT1 §4 | Repositório minirv-dupla-01 (GitHub) | Pendente — ação sua | Exige GitHub/colega/professora |
| R02 | 1 | README: problema, objetivo, ferramentas, como executar, divisão de responsabilidades | HT1 §9 | README.md | Implementado | README criado; nomes dos integrantes e comando que funcionou ficam para você preencher |
| R03 | 1 | Diagrama: memória de instruções, PC, decodificador, registradores, ULA, memória de dados, trace | HT1 §9 | docs/arquitetura.md | Implementado | Diagrama Mermaid em docs/arquitetura.md |
| R04 | 1 | Issue S01 'Criar núcleo mínimo e primeiro programa' | HT1 §9 | Issue no GitHub | Pendente — ação sua | Exige GitHub/colega/professora |
| R05 | 1 | Branch feature/s01-nucleo-minimo | HT1 §9 | Branch (histórico git) | Implementado | Branch feature/s01-nucleo-minimo no repositório local |
| R06 | 1 | Estrutura mínima: minirv/{registers,alu,decoder,cpu,trace}.py, programs/soma.hex, tests/, docs/ | HT1 §5 | Árvore do repositório | Testado e aprovado | 26 testes passando (pytest -q) na Semana 1 |
| R07 | 1 | Programa soma 5+7 → x3=12 executado por `python -m minirv.cpu programs/soma.hex` | HT1 §6-7 | programs/soma.hex, tests/test_cpu.py | Testado e aprovado | 26 testes passando (pytest -q) na Semana 1 |
| R08 | 1 | Trace JSON por instrução (pc, instruction, registers_read, registers_written, next_pc) | HT1 §8 | minirv/trace.py, tests/test_cpu.py | Testado e aprovado | 26 testes passando (pytest -q) na Semana 1 |
| R09 | 1 | Testes de ADD (ULA) e da invariante x0=0 | HT1 §9 | tests/test_alu.py, tests/test_registers.py | Testado e aprovado | 26 testes passando (pytest -q) na Semana 1 |
| R10 | 1 | Execução passo a passo e contínua | HT1 §2 | CPU.step/run e flag --step | Testado e aprovado | step()/run() testados; a flag --step (interativa) foi escrita mas não é coberta por teste automático |
| R11 | 1 | PR revisada pelo colega e tag s01 | HT1 §9 | PR + tag no GitHub | Pendente — ação sua | Exige GitHub/colega/professora |
| R12 | 2 | benchmarks/baseline/ com comando, entrada, configuração e resultados brutos (3 execuções) | HT2 §2-3 | benchmarks/baseline/* | Testado e aprovado | 33 testes passando; resultados brutos de 3 execuções em benchmarks/baseline/ |
| R13 | 2 | orcamento-de-desempenho.md com 11 seções, fórmulas e separação arquitetura × hospedeiro | HT2 §4-8 | docs/semanas/Semana-02/orcamento-de-desempenho.md | Implementado | Documentos preenchidos com valores medidos; seção 10 (contribuições) deixada para a dupla |
| R14 | 2 | ADR-002 (métricas e limites) | HT2 §9 | docs/adr/ADR-002-metricas-e-limites.md | Implementado | Documentos preenchidos com valores medidos; seção 10 (contribuições) deixada para a dupla |
| R15 | 2 | Testes do coletor de métricas (3 repetições, campos numéricos não negativos) | HT2 §10 | tests/test_baseline.py | Testado e aprovado | 33 testes passando; resultados brutos de 3 execuções em benchmarks/baseline/ |
| R16 | 2 | Issue, branch, PR revisada e tag s02 | HT2 §11-12 | GitHub | Pendente — ação sua | Issue, PR revisada e tag s02 no GitHub |
| R17 | 3 | Estrutura de pastas: src(→minirv)/tests/workloads/control/benchmarks/docs/adr/docs/semanas/evidencias | LAB3 §4 | Árvore do repositório | Implementado | Pastas criadas (minirv/ no lugar de src/, ver ADR-001); README atualizado |
| R18 | 3 | README básico (dupla, objetivo, linguagem, comandos) | LAB3 §4 | README.md | Implementado | Pastas criadas (minirv/ no lugar de src/, ver ADR-001); README atualizado |
| R19 | 3 | Módulo word32: normalizar, unsigned, signed, hex, binário, extensão de sinal, soma32 | LAB3 §4-5 | minirv/word32.py | Testado e aprovado | 27 testes novos em tests/test_word32.py; suíte: 60 aprovados |
| R20 | 3 | Testes dos casos-limite (0, -1, 2^31-1, -2^31, 0xFFFFFFFF+1, 0x2A) | LAB3 §6 | tests/test_word32.py | Testado e aprovado | 27 testes novos em tests/test_word32.py; suíte: 60 aprovados |
| R21 | 3 | Relatório da Semana 03 (máscara, overflow, tabela de casos-limite) | LAB3 §4 | docs/semanas/Semana-03/relatorio-semana-03.md | Implementado | Tabela de casos-limite gerada pelo próprio módulo; nomes/data pendentes |
| R22 | 3 | Branch, commit, PR revisada e tag s03 | LAB3 §4 | GitHub | Pendente — ação sua | PR revisada e tag s03 no GitHub |
| R23 | 4 | Portas AND/OR/NOT/XOR com validação + tabelas-verdade + derivação SOP do XOR | S4 §4 | minirv/combinacional/gates.py, docs/logica/tabelas-verdade.md | Testado e aprovado | 52 testes novos; suíte: 112 aprovados; tabelas .md verificadas por teste |
| R24 | 4 | Multiplexador 2:1 (sel inválido gera erro) | S4 §5 | minirv/combinacional/mux.py | Testado e aprovado | 52 testes novos; suíte: 112 aprovados; tabelas .md verificadas por teste |
| R25 | 4 | Decodificador 2→4 (uma e somente uma saída ativa) | S4 §6 | minirv/combinacional/decoder.py | Testado e aprovado | 52 testes novos; suíte: 112 aprovados; tabelas .md verificadas por teste |
| R26 | 4 | decode_control(opcode) para R, I, LOAD, STORE, BRANCH; opcode inválido gera erro | S4 §7 | minirv/combinacional/control.py | Testado e aprovado | 52 testes novos; suíte: 112 aprovados; tabelas .md verificadas por teste |
| R27 | 4 | Testes automatizados com entrada inválida em cada bloco que valida | S4 §8 | tests/test_{gates,mux,decoder,control}.py | Testado e aprovado | 52 testes novos; suíte: 112 aprovados; tabelas .md verificadas por teste |
| R28 | 4 | docs/logica/tabelas-verdade.md e sinais-controle.md | S4 §9 | docs/logica/* | Implementado | docs/logica/*, relatório e diagrama com blocos combinacionais marcados |
| R29 | 4 | Relatório da Semana 04 | S4 §9 | docs/semanas/Semana-04/relatorio-semana-04.md | Implementado | docs/logica/*, relatório e diagrama com blocos combinacionais marcados |
| R30 | 4 | Diagrama arquitetural marcando blocos combinacionais | S4 §9 | docs/arquitetura.md | Implementado | docs/logica/*, relatório e diagrama com blocos combinacionais marcados |
| R31 | 4 | PR revisada e tag s04 | S4 §10-12 | GitHub | Pendente — ação sua | PR revisada e tag s04 no GitHub (só após merge de verdade) |
| R32 | 5 | simulacao-sequencial.md: ≥5 experimentos com previsão e resultado no simulador | S5 §3 | docs/semanas/Semana-05/simulacao-sequencial.md | Pendente — ação sua | Previsões e resultados do projeto preenchidos; resultados do simulador web precisam ser executados e preenchidos por você |
| R33 | 5 | ALU de 32 bits: ADD, SUB, AND, OR, XOR, SLT, SLL, SRL (normal, limite, negativos, overflow) | S5 P4 | minirv/alu.py, tests/test_alu.py | Testado e aprovado | 92 testes novos; suíte: 204 aprovados |
| R34 | 5 | Banco de 32 registradores: read2, write com enable, x0 imutável, índice inválido | S5 P5 | minirv/registers.py, tests/test_registers.py | Testado e aprovado | 92 testes novos; suíte: 204 aprovados |
| R35 | 5 | ProgramCounter: value, advance(+4), jump, reset | S5 P6 | minirv/pc.py, tests/test_pc.py | Testado e aprovado | 92 testes novos; suíte: 204 aprovados |
| R36 | 5 | Testes de comparação e desvio (igualdade e signed) | S5 P7 | tests/test_alu.py | Testado e aprovado | 92 testes novos; suíte: 204 aprovados |
| R37 | 5 | Mapa operação → entrada → saída → sinal | S5 P8 | docs/semanas/Semana-05/mapa-operacoes.md | Implementado | Mapa gerado executando os componentes; relatório com invariantes ↔ testes |
| R38 | 5 | Sequência de testes leitura→cálculo→escrita (x1=5, x2=7, x3=12) | S5 P9 | tests/test_sequencia.py | Testado e aprovado | 92 testes novos; suíte: 204 aprovados |
| R39 | 5 | Relatório da Semana 05 (invariantes, cobertura, limitações) | S5 P11 | docs/semanas/Semana-05/relatorio-semana-05.md | Implementado | Mapa gerado executando os componentes; relatório com invariantes ↔ testes |
| R40 | 5 | PR revisada e tag s05 | S5 P12 | GitHub | Pendente — ação sua | PR revisada e tag s05 no GitHub |
| R41 | 6 | Laboratório da Semana 06 executado e trace-laboratorio salvo | S6 P1 | docs/semanas/Semana-06/trace-laboratorio.json | Pendente — ação sua | Laboratório web da Semana 06 e exportação do trace-laboratorio.json |
| R42 | 6 | Memória de instruções (read_word) | S6 P3 | minirv/instruction_memory.py | Testado e aprovado | 47 testes novos; suíte: 251 aprovados; trace-projeto.json com 15 eventos |
| R43 | 6 | Memória de dados (read/write word, alinhamento, faixa, erro com endereço e causa) | S6 P3 | minirv/data_memory.py | Testado e aprovado | 47 testes novos; suíte: 251 aprovados; trace-projeto.json com 15 eventos |
| R44 | 6 | interfaces-barramento.md refletindo o código | S6 P4 | docs/semanas/Semana-06/interfaces-barramento.md | Implementado | Documentos criados; comparação manual × automático coincide nos 4 itens; diagrama em Mermaid |
| R45 | 6 | Estados FETCH/DECODE/EXECUTE/MEMORY/WRITEBACK observáveis | S6 P5 | minirv/executor.py | Testado e aprovado | 47 testes novos; suíte: 251 aprovados; trace-projeto.json com 15 eventos |
| R46 | 6 | Microssequência de 3 instruções controladas (estado inicial e final obrigatórios) | S6 P6 | minirv/executor.py, tests/test_executor.py | Testado e aprovado | 47 testes novos; suíte: 251 aprovados; trace-projeto.json com 15 eventos |
| R47 | 6 | verificacao-manual.md | S6 P7 | docs/semanas/Semana-06/verificacao-manual.md | Implementado | Documentos criados; comparação manual × automático coincide nos 4 itens; diagrama em Mermaid |
| R48 | 6 | Rastro arquitetural JSON do projeto (seq, pc, word, stage, signals, operands, change) | S6 P8 | docs/semanas/Semana-06/trace-projeto.json | Testado e aprovado | 47 testes novos; suíte: 251 aprovados; trace-projeto.json com 15 eventos |
| R49 | 6 | Testes de alinhamento e acessos inválidos | S6 P9 | tests/test_data_memory.py | Testado e aprovado | 47 testes novos; suíte: 251 aprovados; trace-projeto.json com 15 eventos |
| R50 | 6 | Relatório com comparação manual × automático e total de testes | S6 P10/12 | docs/semanas/Semana-06/relatorio-semana-06.md | Implementado | Documentos criados; comparação manual × automático coincide nos 4 itens; diagrama em Mermaid |
| R51 | 6 | Diagrama do ciclo (PC, imem, controle, registradores, ULA, dmem) | S6 P11 | docs/semanas/Semana-06/diagrama-ciclo.md | Implementado | Documentos criados; comparação manual × automático coincide nos 4 itens; diagrama em Mermaid |
| R52 | 6 | PR revisada e tag s06 | S6 P13 | GitHub | Pendente — ação sua | PR revisada e tag s06 no GitHub |
| R53 | 7 | Simulador da Semana 07 executado e vetores exportados | S7 P1 | docs/semanas/Semana-07/vetores-simulador.json | Pendente |  |
| R54 | 7 | rv32i-subset-v1.md com as 19 instruções e tabela completa de codificação | S7 P3 | docs/isa/rv32i-subset-v1.md | Pendente |  |
| R55 | 7 | Layouts R, I, S, B, U e J documentados com posição e largura | S7 P4 | docs/isa/rv32i-subset-v1.md §2 | Pendente |  |
| R56 | 7 | Sintaxe, registradores, imediatos, rótulos e mensagens de erro | S7 P5 | docs/isa/rv32i-subset-v1.md §4 | Pendente |  |
| R57 | 7 | encode e decode usando a mesma especificação do contrato | S7 P6 | minirv/isa.py, encoder.py, decoder.py | Pendente |  |
| R58 | 7 | ≥1 vetor válido por instrução (19) | S7 P7 | tests/vectors/rv32i-v1.json | Pendente |  |
| R59 | 7 | Testes negativos: registrador inválido, imediato fora da faixa, opcode/funct não suportado | S7 P7 | tests/test_isa_negativos.py | Pendente |  |
| R60 | 7 | Propriedade encode → decode preserva mnemônico e campos | S7 P8 | tests/test_isa_vetores.py, test_isa_roundtrip.py | Pendente |  |
| R61 | 7 | mapeamento-carga-isa.md | S7 P9 | docs/semanas/Semana-07/mapeamento-carga-isa.md | Pendente |  |
| R62 | 7 | Programa Assembly preliminar (leitura, decisão, estado, escrita, laço) | S7 P10 | docs/semanas/Semana-07/controlador-preliminar.s | Pendente |  |
| R63 | 7 | Seção 'Impacto da regularidade' sem afirmar RISC universalmente melhor | S7 P11 | docs/isa/rv32i-subset-v1.md §6 | Pendente |  |
| R64 | 7 | Contrato v1 declarado congelado após revisão + modelo de ADR | S7 P12 | docs/isa/rv32i-subset-v1.md, docs/adr/ADR-TEMPLATE.md | Pendente |  |
| R65 | 7 | Suíte completa sem regressões, PR revisada e tag s07 | S7 P13-14 | GitHub | Pendente |  |
| R66 | 8 | LACUNA: documento da Semana 8 não fornecido (a Semana 07 prevê montador + execução de Assembly) | S7 (intro) | Decisão pendente do usuário | Pendente |  |
| R67 | 8 | Consolidação: suíte completa, matriz, documentação e versão definitiva | Roteiro do usuário | Esta matriz, README, PROJECT_PROGRESS.md | Pendente |  |
| C01 | todas | Palavra de 32 bits; x0-x31; x0 imutável; PC de 32 bits; memória endereçada por byte | S5, S7 | word32, registers, pc, data_memory | Testado e aprovado | word32 (32 bits); registers: x0 imutável; demais itens verificados nas semanas 5 a 7 |
| C02 | todas | Componentes existentes reutilizados, sem duplicação | S7 §2 | Revisão de código (decoder único, ALU única) | Implementado | ProgramCounter e word32 reutilizados; CPU usa ALU/PC/registradores únicos (verificado por revisão de código) |
| C03 | todas | Suíte das semanas anteriores continua passando a cada semana | S5, S6, S7 | pytest -q por semana | Pendente |  |
