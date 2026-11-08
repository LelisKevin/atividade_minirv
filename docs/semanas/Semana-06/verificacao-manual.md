# Verificação manual da microssequência (Semana 06)

Escrita **antes** de rodar o simulador, a partir da especificação do guia. Não deve ser alterada para "bater"
com o resultado automático: se houver diferença, localizar o primeiro evento divergente no rastro.

> As palavras `0x01000001`, `0x02000002` e `0x03000003` são **identificadores didáticos controlados**.
> **Não são codificações RV32I reais.**

**Estado inicial:** x1 = 5, x2 = 7, x3 = 0, x4 = 0, memória[0] = 0, PC = 0x00000000.

| Instrução | Palavra | PC antes | Leituras | Cálculo/ação | Alteração esperada | PC depois |
| --- | --- | --- | --- | --- | --- | --- |
| I1 (x3 ← x1 + x2) | 0x01000001 | 0x00000000 | x1=5; x2=7 | 5 + 7 | x3 = 12 | 0x00000004 |
| I2 (memória[0] ← x3) | 0x02000002 | 0x00000004 | x3=12 | STORE, endereço 0 | memória[0] = 12 | 0x00000008 |
| I3 (x4 ← memória[0]) | 0x03000003 | 0x00000008 | memória[0]=12 | LOAD, endereço 0 | x4 = 12 | 0x0000000C |

**Estado final esperado:** x3 = 12, memória[0] = 12, x4 = 12, PC = 0x0000000C.
