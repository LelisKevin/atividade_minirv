# Tabelas-verdade (especificação da Semana 04)

A tabela é a **especificação**; o código em `minirv/combinacional/` é a implementação;
`tests/` verifica que os dois coincidem (inclusive lendo as tabelas deste arquivo).

## AND, OR e XOR

| A | B | AND | OR | XOR |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

## NOT

| A | NOT |
| --- | --- |
| 0 | 1 |
| 1 | 0 |

## Derivação do XOR por Soma de Produtos (SOP)

Linhas da tabela do XOR em que a saída vale 1: (A=0, B=1) e (A=1, B=0).
Cada linha vira um produto (mintermo) e a função é a soma deles:

- (A=0, B=1) → `¬A · B`
- (A=1, B=0) → `A · ¬B`

**S = ¬A·B + A·¬B**

Conferência pela tabela: (0,0): 1·0 + 0·1 = 0 · (0,1): 1·1 + 0·0 = 1 · (1,0): 0·0 + 1·1 = 1 · (1,1): 0·1 + 1·0 = 0.
Em código: `xor_sop(a, b) = OR(AND(NOT(a), b), AND(a, NOT(b)))`, testado contra `XOR` nas quatro linhas.

## Multiplexador 2:1

| sel | entrada0 | entrada1 | saída |
| --- | --- | --- | --- |
| 0 | 10 | 99 | 10 |
| 1 | 10 | 99 | 99 |

Qualquer `sel` diferente de 0 ou 1 gera `ValueError`.

## Decodificador 2→4

| A | B | código | saída ativa | Y0 | Y1 | Y2 | Y3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 00 | Y0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 01 | Y1 | 0 | 1 | 0 | 0 |
| 1 | 0 | 10 | Y2 | 0 | 0 | 1 | 0 |
| 1 | 1 | 11 | Y3 | 0 | 0 | 0 | 1 |

Para cada combinação válida, uma e somente uma saída vale 1.

## Entradas inválidas

Portas, MUX e decodificador aceitam apenas os inteiros 0 e 1. `True`, `1.0`, `2`, `None` e `"0"` geram
`ValueError`. (Em Python, `True == 1` e `1.0 in (0, 1)`, o que passaria despercebido sem checar o tipo.)
