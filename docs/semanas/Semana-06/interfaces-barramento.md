# Interfaces de barramento (Semana 06)

Reflete o código real (`minirv/executor.py`). Largura 32 bits em todos os caminhos de dados/endereço.

| Origem | Destino | Tipo | Largura | Uso | No código |
| --- | --- | --- | --- | --- | --- |
| PC | Memória de instruções | Endereço | 32 bits | Selecionar a palavra (FETCH) | `ProgramCounter.value()` → `InstructionMemory.read_word(pc)` |
| Memória de instruções | Controle/decodificação | Dados/instrução | 32 bits | Identificar a instrução controlada (DECODE) | `INSTRUCOES_CONTROLADAS[word]` |
| Decodificação | Controle (`decode_control`) | Classe de opcode | 7 bits | Gerar RegWrite, ALUSrc, MemRead, MemWrite, Branch | `decode_control(ins["opcode"])` |
| Registradores | MUX ALUSrc / ULA | Dados | 32 bits | Fornecer operandos A e B | `RegisterFile.read(rs1/rs2)` |
| Decodificação | MUX ALUSrc | Imediato | 32 bits | Segundo operando quando ALUSrc = 1 | `mux2(ALUSrc, reg_b, imm)` |
| Controle | ULA | Controle | 1 bit (ALUSrc) | Escolher registrador ou imediato | `mux2` |
| ULA | Memória de dados | Endereço | 32 bits | Selecionar posição (endereço efetivo) | `execute("ADD", base, imm)` → `DataMemory.*_word(addr)` |
| Registradores | Memória de dados | Dados | 32 bits | Valor de STORE | `DataMemory.write_word(addr, x3)` |
| Memória de dados | Registradores | Dados | 32 bits | Valor de LOAD | `DataMemory.read_word(addr)` → `RegisterFile.write(rd, v)` |
| ULA | Registradores | Dados | 32 bits | Resultado da CADD | `RegisterFile.write(3, resultado)` |
| Controle (RegWrite) | Registradores | Controle | 1 bit | Habilitar escrita | `write(rd, v, enable=True)` |
| WRITEBACK | PC | Controle | — | Avançar PC + 4 ao final da instrução | `ProgramCounter.advance()` |

Regras de uso: endereços inteiros, alinhados em 4 e dentro da faixa; violação gera `MemoryAccessError` com
memória, endereço e causa. Todos os eventos dos estados vão para o rastro (`Trace`).
