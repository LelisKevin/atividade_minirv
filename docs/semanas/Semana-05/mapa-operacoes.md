# Mapa operação → entrada → saída → sinal (Semana 05)

Cada linha foi produzida **executando** o componente correspondente (ALU, `RegisterFile`, `ProgramCounter`);
os mesmos casos estão cobertos por `tests/test_alu.py`, `test_registers.py`, `test_pc.py` e `test_sequencia.py`.
"ALUOp" e "RegWrite" são sinais combinacionais que selecionam o comportamento; na Semana 05 eles são
argumentos de função, e a unidade de controle que os gera de verdade entra na Semana 09.

| Operação/ação | Entrada | Saída esperada | Sinal/decisão |
| --- | --- | --- | --- |
| ADD | a=5; b=7 | 12 (0x0000000C) | ALUOp=ADD |
| ADD | a=4294967295; b=1 | 0 (0x00000000) | ALUOp=ADD (overflow: bit 32 descartado) |
| SUB | a=7; b=5 | 2 (0x00000002) | ALUOp=SUB |
| SUB | a=0; b=1 | 4294967295 (0xFFFFFFFF) | ALUOp=SUB |
| AND | a=4294967295; b=0 | 0 (0x00000000) | ALUOp=AND |
| OR | a=2863311530; b=1431655765 | 4294967295 (0xFFFFFFFF) | ALUOp=OR |
| XOR | a=2863311530; b=1431655765 | 4294967295 (0xFFFFFFFF) | ALUOp=XOR |
| SLT | a=-1; b=1 | 1 (0x00000001) | ALUOp=SLT (comparação com sinal) |
| SLT | a=5; b=5 | 0 (0x00000000) | ALUOp=SLT |
| SLL | a=1; b=31 | 2147483648 (0x80000000) | ALUOp=SLL |
| SRL | a=2147483648; b=31 | 1 (0x00000001) | ALUOp=SRL |
| Escrita x5 | rd=5; value=10 | x5=10 | RegWrite=1 |
| Tentativa em x0 | rd=0; value=10 | x0=0 | RegWrite=1 + invariante x0 |
| Escrita desabilitada | rd=6; value=99; enable=False | x6=0 | RegWrite=0 |
| PC sequencial | PC=0x20 | 0x00000024 | seleção sequencial (PC+4) |
| PC redirecionado | target=0x100 | 0x00000100 | seleção salto/desvio |
| BEQ por composição (taken) | a=5; b=5 → SUB=0 | PC=0x00000100 | Zero=1 → seleciona alvo |
| BLT por composição (taken) | a=-1; b=1 → SLT=1 | PC=0x00000100 | SLT=1 → seleciona alvo |
| BLT por composição (not taken) | a=1; b=-1 → SLT=0 | PC=0x00000024 | SLT=0 → segue sequencial |

## Como ler os desvios

O guia permite testar desvios **por composição**: a ALU produz um valor (`SUB` → 0 para igualdade; `SLT` → 1 para
"menor que" com sinal) e, conforme essa decisão, o PC avança 4 ou salta para o alvo. A lógica de controle completa
(ligar o resultado da ALU ao seletor do PC) fica para a integração futura.
