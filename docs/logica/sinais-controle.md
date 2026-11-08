# Sinais de controle (Semana 04, tabela didática reduzida)

Leitura: 1 significa "ativar/usar"; 0 significa "não ativar/não usar". Para `ALUSrc`, 0 seleciona
registrador e 1 seleciona imediato.

| Instrução | O que precisa fazer | RegWrite | ALUSrc | MemRead | MemWrite | Branch |
| --- | --- | --- | --- | --- | --- | --- |
| ADD | somar dois registradores e gravar o resultado | 1 | 0 | 0 | 0 | 0 |
| ADDI | somar registrador com imediato e gravar | 1 | 1 | 0 | 0 | 0 |
| LW | calcular endereço, ler memória e gravar em registrador | 1 | 1 | 1 | 0 | 0 |
| SW | calcular endereço e escrever na memória | 0 | 1 | 0 | 1 | 0 |
| BEQ | comparar registradores e permitir desvio | 0 | 0 | 0 | 0 | 1 |

## Por que cada sinal vale 0 ou 1 (uma frase por linha)

- **ADD:** grava resultado (`RegWrite=1`) e o segundo operando vem de registrador (`ALUSrc=0`); não toca a memória nem desvia.
- **ADDI:** grava resultado (`RegWrite=1`) e o segundo operando é o imediato (`ALUSrc=1`); não toca a memória nem desvia.
- **LW:** a ULA soma base + deslocamento (imediato, `ALUSrc=1`), a memória é lida (`MemRead=1`) e o valor é gravado no registrador (`RegWrite=1`).
- **SW:** a ULA soma base + deslocamento (imediato, `ALUSrc=1`) e a memória é escrita (`MemWrite=1`); não grava registrador (`RegWrite=0`).
- **BEQ:** compara dois registradores (`ALUSrc=0`) e só habilita o desvio (`Branch=1`); não grava registrador nem acessa dados.

## Opcode → classe (implementação em `minirv/combinacional/control.py`)

| Opcode | Classe | Instruções da tabela |
| --- | --- | --- |
| 0110011 | R | ADD |
| 0010011 | I | ADDI |
| 0000011 | LOAD | LW |
| 0100011 | STORE | SW |
| 1100011 | BRANCH | BEQ |

O opcode identifica só a classe principal. ADD, SUB, AND e OR, por exemplo, compartilham o opcode `0110011`
e serão separados por `funct3`/`funct7` na Semana 07. Opcodes fora destes cinco geram `ValueError`.
