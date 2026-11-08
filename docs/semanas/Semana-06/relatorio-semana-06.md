# Relatório da Semana 06 - Organização funcional e ciclo de instrução

- **Dupla:** _(preencher)_ · **Revisor da PR:** _(preencher)_ · **Branch:** `entrega/semana-06-ciclo-instrucao`

## 1. Objetivo

Responder como os blocos trocam dados e controle durante uma instrução completa: primeiro ciclo executável,
com instruções controladas (identificadores didáticos, **não** codificações RV32I).

## 2. O que foi implementado

`minirv/instruction_memory.py`, `minirv/data_memory.py` (+ `memory_access.py`), `minirv/executor.py` (estados
FETCH/DECODE/EXECUTE/MEMORY/WRITEBACK observáveis via `step_stage()` e rastro). O executor reutiliza o MUX e o
controle da Semana 04 e a ALU, os registradores e o PC da Semana 05. `cpu.py` passou a usar `InstructionMemory`.

## 3. Comparação manual × automático

Manual: `verificacao-manual.md` (escrita antes da execução). Automático: execução de `python -m minirv.executor`.

| Item | Manual | Automático | Coincide? |
| --- | --- | --- | --- |
| x3 | 12 | 12 | sim |
| memória[0] | 12 | 12 | sim |
| x4 | 12 | 12 | sim |
| PC final | 0x0000000C | 0x0000000C | sim |

Nenhum evento divergente. O teste `test_evento_5_igual_ao_exemplo_do_guia` confirma que o evento `seq 5` é idêntico
ao exemplo do roteiro, e `test_rastro_reconstroi_as_alteracoes_de_estado` reconstrói as alterações só pelo rastro.

## 4. Rastro

`docs/semanas/Semana-06/trace-projeto.json`: 15 eventos (5 estados × 3 instruções) com seq, pc, word, stage, signals,
operands e change. O rastro do laboratório da aula (`trace-laboratorio.json`) **não existe**: depende do site da
aula e está pendente (ação da dupla).

## 5. Testes de alinhamento e acesso inválido

`tests/test_data_memory.py` (25) cobre: leitura/escrita válida, endereço 6 desalinhado, abaixo do início (−4, −1),
acima do último endereço com palavra inteira (4096 em memória de 4096; 2³²), não inteiro, ausência de escrita
parcial/truncamento e mensagem com endereço e causa. `tests/test_instruction_memory.py` (9) cobre a memória de instruções.

## 6. Suíte completa

`pytest -q`: **251 testes, 251 aprovados** (204 anteriores + 47 novos: 25 + 9 + 13). Sem regressões.

## 7. Decisões

- Memória de dados de 4 KiB, little-endian, base 0 (ADR-001).
- Eventos de FETCH usam o sinal `IMemRead`; o resultado da ULA aparece em `operands.alu_result` no EXECUTE.
- A "decisão de memória da Semana 01" não estava registrada; ficou no ADR-001 (status Proposto).

## 8. Pendências

Executar o laboratório da aula e salvar `trace-laboratorio.json` (inclui testar endereço válido, desalinhado e fora da
faixa); nomes e revisor; PR revisada e tag `s06`.
