# Mapeamento preliminar da carga para o subconjunto RV32I v1 (Semana 07) — histórico superado

Este documento registra o mapa preliminar da Semana 07 (`0xFFFF0000`) e foi mantido como histórico. Ele não
descreve o mapa MMIO vigente, que usa `0x80000000`, `0x80000004` e `0x80000008`; o programa
`controlador-preliminar.s` também não é compatível com esse mapa atual.

Para cada necessidade do controlador térmico preliminar, este documento registra quais instruções RV32I v1 a expressam.

| Necessidade | Instruções | Justificativa | Onde aparece no programa |
| --- | --- | --- | --- |
| Leitura do sensor | `LUI` + `LW` | No mapa preliminar, `LUI` monta a base 0xFFFF0000 (`LUI x10, 0xFFFF0`): endereços altos não cabem no imediato de 12 bits de `LW`/`ADDI`. `LW rd, imm(rs1)` lê a palavra da E/S com deslocamento de 0 a 2047 bytes, sem instrução especial de E/S. | `LUI x10, 0xFFFF0`; `LW x11, 0(x10)` |
| Decisão por limites | `SLT` / `BLT` / `BEQ` / `BNE` | `SLT` produz 0/1 com sinal (permite guardar o resultado de uma comparação, como no alarme); `BLT` compara e desvia numa instrução só; `BEQ`/`BNE` tratam igualdade e desigualdade (por exemplo, atingir exatamente o total). A comparação "maior ou igual" sai de `BLT` com operandos trocados ou de `SLT` + `XOR` com 1, então não precisa de `BGE` no contrato. | `SLT x13, x11, x17`; `BLT x11, x15, abaixo`; `BLT x16, x11, escreve` |
| Preservar/alterar estado | operações R / `ADDI` (+ `XOR`) | O estado do atuador fica num registrador. `ADDI x12, x0, 1/0` altera; **não escrever** nada preserva (a histerese acontece desviando por cima das instruções que alterariam). `ADD/SUB/AND/OR/XOR` e `ADDI/ANDI/ORI` cobrem inversão de bit, contadores e máscaras. | `ADDI x12, x0, 1`; `XOR x13, x13, x20` |
| Escrever atuador | `LUI` + `SW` | Mesma base montada por `LUI`; `SW rs2, imm(rs1)` grava o estado (x12) no endereço base + 4. | `SW x12, 4(x10)` |
| Registrar alarme | `LUI` + `SW` | Idem, no endereço base + 8, gravando o bit calculado por `SLT`/`XOR`. | `SW x13, 8(x10)` |
| Repetir laço | branches / `JAL` | `BLT` fecha o laço enquanto o índice lido for menor que o total (condição de continuidade); `JAL x0, rótulo` é um desvio incondicional que descarta o endereço de retorno (usa `x0`) e serve para pular blocos e para o laço final. | `BLT x14, x18, loop`; `JAL x0, escreve`; `JAL x0, fim` |

## Onde `JALR` e `LUI` entram

- `JALR` não é necessário para este controlador (não há sub-rotinas nem endereços calculados); permanece no contrato por ser
  a única forma de retorno e de salto para endereço em registrador (`JALR x0, 0(x1)` = retornar).
- `ANDI`/`ORI` permitem isolar ou ligar bits de um registrador de status, caso a E/S empacote o atuador e o alarme numa
  mesma palavra (não é o caso da premissa atual).

## Limites do mapeamento

- A faixa de `BLT` é ±4 KiB e a de `JAL` é ±1 MiB; o programa é muito menor que isso.
- Constantes até 2047 cabem em `ADDI`; maiores exigem `LUI + ADDI`.
- O programa foi conferido só por teste de sintaxe contra o contrato (`tests/test_controlador_preliminar.py`);
  **não foi executado**, porque a execução de Assembly é da Semana 08.
