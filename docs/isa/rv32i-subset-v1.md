# Contrato do subconjunto RV32I do MiniRV — versão 1

**Status: v1 CANDIDATA A CONGELAMENTO** (vetores e testes passando; aguardando revisão cruzada da PR).
Ao aprovar a PR, trocar esta linha por `Status: v1 CONGELADA` (ver seção 8).

Este arquivo é a **fonte única de verdade** do subconjunto implementado. A tabela da seção 3 é lida em tempo de
execução por `minirv/isa.py`; `minirv/encoder.py` e `minirv/decoder.py` usam essa mesma especificação, sem tabela
duplicada. Alterar a tabela altera o código (e pode quebrar os vetores, o que é intencional).

## 1. Regras gerais

- Palavra de 32 bits; registradores x0 a x31; x0 sempre 0; PC de 32 bits; memória endereçada por byte,
  palavras em little-endian (ADR-001).
- Toda instrução ocupa 32 bits e o PC avança de 4 em 4. **Não há extensão de instruções comprimidas.**
- Decisão do MiniRV (mais estrita que o RV32I): offsets de `BEQ/BNE/BLT` e `JAL` devem ser **múltiplos de 4**
  (o RV32I admite múltiplos de 2). O mesmo vale para o alvo de `JALR` em execução (PC desalinhado é erro).
- `SLL` e `SRL` são deslocamentos por registrador: a quantidade é `rs2[4:0]` (0 a 31). `SRL` é lógico.
- `SLT` compara com sinal (complemento de dois). `BLT` também compara com sinal.
- Acessos de `LW`/`SW` são de palavra inteira e alinhados em 4 (violação é erro de memória, Semana 06).
- Fora do subconjunto (portanto "não suportado"): `ecall`, `SLLI/SRLI/SRAI`, `SRA`, `SLTI`, `XORI`, `LB/LH/SB/SH`,
  `BGE/BLTU/BGEU`, `AUIPC`, multiplicação e divisão.

## 2. Layouts dos seis formatos (bit 31 → bit 0)

**R** — `funct7 | rs2 | rs1 | funct3 | rd | opcode`

| Campo | funct7 | rs2 | rs1 | funct3 | rd | opcode |
| --- | --- | --- | --- | --- | --- | --- |
| Bits | 31:25 | 24:20 | 19:15 | 14:12 | 11:7 | 6:0 |
| Largura | 7 | 5 | 5 | 3 | 5 | 7 |

**I** — `imm[11:0] | rs1 | funct3 | rd | opcode`

| Campo | imm[11:0] | rs1 | funct3 | rd | opcode |
| --- | --- | --- | --- | --- | --- |
| Bits | 31:20 | 19:15 | 14:12 | 11:7 | 6:0 |
| Largura | 12 | 5 | 3 | 5 | 7 |

**S** — `imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode`

| Campo | imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode |
| --- | --- | --- | --- | --- | --- | --- |
| Bits | 31:25 | 24:20 | 19:15 | 14:12 | 11:7 | 6:0 |
| Largura | 7 | 5 | 5 | 3 | 5 | 7 |

**B** — `imm[12|10:5] | rs2 | rs1 | funct3 | imm[4:1|11] | opcode`

| Campo | imm[12] | imm[10:5] | rs2 | rs1 | funct3 | imm[4:1] | imm[11] | opcode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bits | 31 | 30:25 | 24:20 | 19:15 | 14:12 | 11:8 | 7 | 6:0 |
| Largura | 1 | 6 | 5 | 5 | 3 | 4 | 1 | 7 |

O bit 0 do deslocamento não é armazenado (é sempre 0); o deslocamento tem 13 bits com sinal.

**U** — `imm[31:12] | rd | opcode`

| Campo | imm[31:12] | rd | opcode |
| --- | --- | --- | --- |
| Bits | 31:12 | 11:7 | 6:0 |
| Largura | 20 | 5 | 7 |

**J** — `imm[20|10:1|11|19:12] | rd | opcode`

| Campo | imm[20] | imm[10:1] | imm[11] | imm[19:12] | rd | opcode |
| --- | --- | --- | --- | --- | --- | --- |
| Bits | 31 | 30:21 | 20 | 19:12 | 11:7 | 6:0 |
| Largura | 1 | 10 | 1 | 8 | 5 | 7 |

O bit 0 do deslocamento não é armazenado; o deslocamento tem 21 bits com sinal.

## 3. Tabela de codificação (lida por `minirv/isa.py`)

Formato de leitura: `funct3`/`funct7` em binário (`—` = não se aplica); `Faixa/restrição` usa `imm: mín..máx` e
`múltiplo de N` (decimal). Nas instruções com `imm(rs1)` o imediato é o deslocamento em bytes. Em `BEQ/BNE/BLT/JAL`
o `imm` é o deslocamento **em bytes relativo ao PC da própria instrução** (um rótulo é convertido para isso pelo
montador, Semana 08). Em `LUI` o `imm` é o valor do campo de 20 bits (o efeito é `imm << 12`).

<!-- ISA-TABLE:BEGIN -->
| Mnemônico | Formato | Sintaxe | opcode | funct3 | funct7 | Campos | Faixa/restrição | Semântica | Erro esperado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADD | R | ADD rd, rs1, rs2 | 0110011 | 000 | 0000000 | rd, rs1, rs2 | — | rd ← rs1 + rs2 (32 bits, overflow descartado) | registrador inválido; campo incompatível |
| SUB | R | SUB rd, rs1, rs2 | 0110011 | 000 | 0100000 | rd, rs1, rs2 | — | rd ← rs1 − rs2 | registrador inválido; campo incompatível |
| SLL | R | SLL rd, rs1, rs2 | 0110011 | 001 | 0000000 | rd, rs1, rs2 | — | rd ← rs1 << rs2[4:0] | registrador inválido; campo incompatível |
| SLT | R | SLT rd, rs1, rs2 | 0110011 | 010 | 0000000 | rd, rs1, rs2 | — | rd ← 1 se rs1 < rs2 (com sinal), senão 0 | registrador inválido; campo incompatível |
| XOR | R | XOR rd, rs1, rs2 | 0110011 | 100 | 0000000 | rd, rs1, rs2 | — | rd ← rs1 XOR rs2 | registrador inválido; campo incompatível |
| SRL | R | SRL rd, rs1, rs2 | 0110011 | 101 | 0000000 | rd, rs1, rs2 | — | rd ← rs1 >> rs2[4:0] (lógico) | registrador inválido; campo incompatível |
| OR | R | OR rd, rs1, rs2 | 0110011 | 110 | 0000000 | rd, rs1, rs2 | — | rd ← rs1 OR rs2 | registrador inválido; campo incompatível |
| AND | R | AND rd, rs1, rs2 | 0110011 | 111 | 0000000 | rd, rs1, rs2 | — | rd ← rs1 AND rs2 | registrador inválido; campo incompatível |
| ADDI | I | ADDI rd, rs1, imm | 0010011 | 000 | — | rd, rs1, imm | imm: -2048..2047 | rd ← rs1 + imm (imm estendido com sinal) | registrador inválido; imediato fora da faixa |
| ORI | I | ORI rd, rs1, imm | 0010011 | 110 | — | rd, rs1, imm | imm: -2048..2047 | rd ← rs1 OR imm (imm estendido com sinal) | registrador inválido; imediato fora da faixa |
| ANDI | I | ANDI rd, rs1, imm | 0010011 | 111 | — | rd, rs1, imm | imm: -2048..2047 | rd ← rs1 AND imm (imm estendido com sinal) | registrador inválido; imediato fora da faixa |
| LW | I | LW rd, imm(rs1) | 0000011 | 010 | — | rd, rs1, imm | imm: -2048..2047 | rd ← mem32[rs1 + imm]; endereço alinhado em 4 | registrador inválido; imediato fora da faixa; erro de memória |
| JALR | I | JALR rd, imm(rs1) | 1100111 | 000 | — | rd, rs1, imm | imm: -2048..2047 | rd ← PC + 4; PC ← (rs1 + imm) com bit 0 zerado; alvo múltiplo de 4 | registrador inválido; imediato fora da faixa; PC desalinhado |
| SW | S | SW rs2, imm(rs1) | 0100011 | 010 | — | rs1, rs2, imm | imm: -2048..2047 | mem32[rs1 + imm] ← rs2; endereço alinhado em 4 | registrador inválido; imediato fora da faixa; erro de memória |
| BEQ | B | BEQ rs1, rs2, imm | 1100011 | 000 | — | rs1, rs2, imm | imm: -4096..4092; múltiplo de 4 | se rs1 == rs2: PC ← PC + imm | registrador inválido; imediato fora da faixa ou desalinhado |
| BNE | B | BNE rs1, rs2, imm | 1100011 | 001 | — | rs1, rs2, imm | imm: -4096..4092; múltiplo de 4 | se rs1 != rs2: PC ← PC + imm | registrador inválido; imediato fora da faixa ou desalinhado |
| BLT | B | BLT rs1, rs2, imm | 1100011 | 100 | — | rs1, rs2, imm | imm: -4096..4092; múltiplo de 4 | se rs1 < rs2 (com sinal): PC ← PC + imm | registrador inválido; imediato fora da faixa ou desalinhado |
| JAL | J | JAL rd, imm | 1101111 | — | — | rd, imm | imm: -1048576..1048572; múltiplo de 4 | rd ← PC + 4; PC ← PC + imm | registrador inválido; imediato fora da faixa ou desalinhado |
| LUI | U | LUI rd, imm | 0110111 | — | — | rd, imm | imm: 0..1048575 | rd ← imm << 12 | registrador inválido; imediato fora da faixa |
<!-- ISA-TABLE:END -->

Escritas em `x0` são aceitas na codificação (por exemplo `JAL x0, ...` descarta o endereço de retorno) e ignoradas
na execução.

## 4. Sintaxe, registradores, imediatos e rótulos (regras para o montador da Semana 08)

- **Registradores:** `x0` a `x31` (minúsculo ou maiúsculo). Nomes ABI (`a0`, `sp`...) **não** fazem parte da v1.
- **Mnemônicos:** maiúsculos ou minúsculos; um comando por linha; operandos separados por vírgula.
- **Formas:** R `ADD x3, x1, x2` · imediata `ADDI x1, x0, 5` · LOAD `LW x11, 0(x10)` · STORE `SW x12, 4(x10)` ·
  branch `BEQ x1, x2, rotulo` · `LUI x10, 0xFFFF0` · `JAL x0, rotulo` · `JALR x0, 0(x1)`.
  Em STORE o primeiro operando é o registrador **fonte** (`rs2`).
- **Imediatos:** decimal (`-4`, `12`) ou hexadecimal com prefixo `0x` (`0xFF`, `0xFFFF0`); sinal `-` permitido em decimal.
  Em hexadecimal o valor é interpretado como número, sem extensão de sinal implícita (`0xFFF` em `ADDI` vale 4095 e
  é **fora da faixa**).
- **Faixas e alinhamento:** os da coluna "Faixa/restrição". Deslocamentos de branch/jump devem ser múltiplos de 4.
- **Rótulos:** identificador `[A-Za-z_][A-Za-z0-9_]*` seguido de `:` no início da linha (pode vir sozinho). Só
  `BEQ/BNE/BLT/JAL` aceitam rótulo no lugar do imediato; o valor codificado é `endereço(rótulo) − endereço(instrução)`.
  Rótulo indefinido ou duplicado é erro. Comentários começam com `#`.

## 5. Mensagens de erro (usadas por `minirv/encoder.py` e `minirv/decoder.py`)

Todas as exceções herdam de `ISAError` (que é `ValueError`) e nada é aceito em silêncio.

| Situação | Exceção | Mensagem (modelo) |
| --- | --- | --- |
| Registrador fora de 0–31 ou não inteiro | `InvalidRegisterError` | `registrador inválido: x32 no campo rs1 de ADD (válidos: x0 a x31)` |
| Imediato fora da faixa | `ImmediateRangeError` | `imediato fora da faixa: 4096 em ADDI (aceito: -2048 a 2047)` |
| Imediato desalinhado | `ImmediateRangeError` | `imediato desalinhado: 6 em BEQ (exige múltiplo de 4)` |
| Imediato não inteiro | `ImmediateRangeError` | `imediato inválido em ADDI: '5' (esperado inteiro)` |
| Mnemônico fora do subconjunto | `UnsupportedInstructionError` | `instrução não suportada: MUL` |
| Palavra com opcode/funct não suportado | `UnsupportedInstructionError` | `instrução não suportada: 0x02208033 (opcode=0110011, funct3=000, funct7=0000001)` |
| Campo que o formato não possui (ex.: `rd` em SW) | `FieldMismatchError` | `campo incompatível: SW não possui rd` |
| Campo obrigatório ausente | `FieldMismatchError` | `campo ausente: ADD exige rs2` |
| `format` informado diferente do formato da instrução | `FieldMismatchError` | `campo incompatível: format 'I' em ADD (formato correto: R)` |
| Palavra que não é inteiro de 32 bits | `InvalidWordError` | `palavra inválida (esperado inteiro de 32 bits): 4294967296` |

## 6. Impacto da regularidade

Escopo: as 19 instruções deste contrato e o MiniRV. Não é uma comparação geral entre arquiteturas.

| Aspecto | O que a regularidade traz | Custo / trade-off |
| --- | --- | --- |
| **Decodificação** | Comprimento fixo (32 bits) e `opcode`, `rd`, `rs1`, `rs2`, `funct3` nas mesmas posições em todos os formatos: o decodificador extrai campos sem saber o formato antes (`decode` faz isso em poucas linhas) e sabe onde a próxima instrução começa. | O imediato **não** é regular: em B e J os bits ficam embaralhados para manter `rs1/rs2/rd` fixos. Em formatos com comprimento variável a decodificação de tamanho tem de ser feita antes de achar os campos. |
| **Caminho de dados** | Operandos quase sempre em registradores e só `LW/SW` acessam memória: poucos caminhos, um banco com duas leituras e uma escrita, e um único somador serve para aritmética e para endereço efetivo (Semana 06). | Operações com operando em memória exigem sequências (carregar, operar, gravar); o estado vive nos registradores, então há mais tráfego entre registradores e memória. |
| **Instruções por operação complexa** | Operações simples e uniformes são compostas pelo software. | Mais instruções: constante de 32 bits = `LUI + ADDI`; somar na memória = `LW + ADD + SW`; chamar rotina = `JAL`/`JALR` mais salvar/restaurar registradores à mão. |
| **Tamanho do código** | Tamanho previsível (4 bytes × nº de instruções), simples de calcular e de endereçar. | Tende a ocupar mais memória do que um conjunto com instruções curtas ou de comprimento variável para o mesmo programa; a diferença depende do programa e não foi medida aqui. |
| **Facilidade de testar o contrato** | Uma tabela só descreve tudo; encode e decode podem ser testados por ida e volta e por um vetor por instrução; formatos fixos viabilizam geração aleatória de casos (`tests/test_isa_roundtrip.py`). | Os testes precisam cobrir o embaralhamento dos imediatos (limites de B e J) e as combinações `opcode/funct` inválidas. |

Conclusão dentro do escopo: a regularidade reduz a complexidade do hardware e dos testes **ao custo de** mais instruções
e, em geral, mais bytes de código por tarefa. Conjuntos de instruções de comprimento variável ou com operandos em
memória escolhem outro ponto desse equilíbrio (código mais denso e menos instruções, com decodificação e caminho de
dados mais complexos). Qual é melhor depende da carga, da implementação e da métrica (desempenho, área, energia,
densidade). Este documento não afirma que um dos estilos seja superior em geral.

## 7. Carga canônica

O mapeamento entre as necessidades da carga canônica (controlador térmico) e as instruções deste contrato está em
`docs/semanas/Semana-07/mapeamento-carga-isa.md`; o programa preliminar, em `controlador-preliminar.s`.

## 8. Versão, congelamento e mudanças

- **v1** reúne exatamente as 19 instruções da seção 3; nada foi acrescentado para "aumentar a quantidade".
- **Para congelar:** depois que a PR for revisada pela dupla e os vetores passarem, substituir a linha de status do
  topo por `Status: v1 CONGELADA` e registrar a data.
- **Depois de congelada,** qualquer mudança de instrução, sintaxe, codificação ou semântica exige um ADR
  (`docs/adr/ADR-TEMPLATE.md`) com motivo, impacto em encode/decode, testes e Assembly, e decisão.
