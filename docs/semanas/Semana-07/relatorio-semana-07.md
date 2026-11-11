# Relatório da Semana 07 - Contrato do subconjunto RV32I (v1)

> **Registro histórico:** o mapa MMIO `0xFFFF0000` mencionado neste relatório e no programa preliminar foi
> superado. O mapa atual está documentado em `docs/adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md`;
> a memória e o subconjunto atual da CPU suportam os acessos `LW`/`SW` ao MMIO por meio do reatômetro.

- **Dupla:** _(preencher)_ · **Revisor da PR:** _(preencher)_ · **Branch:** `entrega/semana-07-isa-rv32i`

## 1. Pergunta PBL e objetivo

Qual conjunto mínimo de instruções é suficiente para expressar a carga de controle e manter decodificação regular?
Entrega: contrato da ISA (19 instruções) + vetores encode/decode + programa Assembly preliminar. O montador completo
e a execução de Assembly **não** foram feitos (são da Semana 08, conforme o guia).

## 2. O que foi entregue

| Entregável | Arquivo |
| --- | --- |
| Contrato v1 (tabela de codificação, 6 layouts, sintaxe, erros, regularidade) | `docs/isa/rv32i-subset-v1.md` |
| Leitura do contrato (fonte única) | `minirv/isa.py` |
| encode / decode | `minirv/encoder.py`, `minirv/decoder.py` |
| Vetores válidos e negativos | `tests/vectors/rv32i-v1.json` (43 vetores), `rv32i-v1-negativos.json` (43 casos) |
| Mapeamento da carga canônica | `docs/semanas/Semana-07/mapeamento-carga-isa.md` |
| Programa preliminar | `docs/semanas/Semana-07/controlador-preliminar.s` |
| Modelo de ADR | `docs/adr/ADR-TEMPLATE.md` |

## 3. Vetores por instrução

| Instrução | Formato | Opcode | Vetores |
| --- | --- | --- | --- |
| ADD | R | 0x33 | 2 |
| SUB | R | 0x33 | 2 |
| SLL | R | 0x33 | 1 |
| SLT | R | 0x33 | 1 |
| XOR | R | 0x33 | 1 |
| SRL | R | 0x33 | 1 |
| OR | R | 0x33 | 1 |
| AND | R | 0x33 | 1 |
| ADDI | I | 0x13 | 4 |
| ORI | I | 0x13 | 2 |
| ANDI | I | 0x13 | 2 |
| LW | I | 0x03 | 3 |
| JALR | I | 0x67 | 3 |
| SW | S | 0x23 | 4 |
| BEQ | B | 0x63 | 2 |
| BNE | B | 0x63 | 2 |
| BLT | B | 0x63 | 2 |
| JAL | J | 0x6F | 5 |
| LUI | U | 0x37 | 4 |

## 4. Como a regra "mesma especificação" foi cumprida

`minirv/isa.py` lê a tabela do próprio `rv32i-subset-v1.md`; encode e decode consultam só `SPEC`. Não existe tabela de
opcodes no código. O teste `test_alterar_o_contrato_altera_a_especificacao` mostra que mudar o `.md` muda o que o
código enxerga, e `test_load_spec_*` mostram que um contrato malformado (instrução faltando/duplicada/a mais,
opcode com largura errada, marcadores ausentes) é recusado na leitura.

## 5. Verificação

- **Ida e volta** (`test_isa_roundtrip.py`): 500 instruções aleatórias por mnemônico, todos os 32 registradores,
  limites dos imediatos, e uma propriedade inversa: de 200.000 palavras aleatórias, toda palavra que decodifica é
  recodificada idêntica. O decodificado traz só campos do formato (SW sem `rd`, LUI sem `rs1`/`rs2`).
- **Vetores** (`test_isa_vetores.py`): palavra produzida, volta por decode e sintaxe canônica.
- **Negativos** (`test_isa_negativos.py`): registrador inválido, imediato fora da faixa e desalinhado,
  opcode/funct não suportado (MUL, ECALL, LB, SLLI, SRA, BGE, JALR com funct3 errado), campos incompatíveis/ausentes.
- **Referência externa** (`test_isa_contrato.py`): opcode/funct3/funct7 do contrato conferidos contra as
  codificações do manual RISC-V digitadas de forma independente.
- **Desassemblador independente** (`test_isa_capstone.py`, opcional): os 43 vetores foram desmontados pelo capstone
  (mnemônico, registradores e imediatos coincidem, inclusive nos extremos de B e J).
- **Mutação:** quebrei de propósito a codificação de B, a de J, o `funct7` do SUB no contrato e a faixa do ADDI; a
  suíte falhou nos quatro casos (e foi restaurada).
- **Programa preliminar** (`test_controlador_preliminar.py`): mnemônicos, operandos, faixas, rótulos e deslocamentos
  conferidos contra o contrato; cobre leitura, decisão, estado, escrita e laço. **Não foi executado.**

## 6. Decisões do contrato

- Deslocamentos de B e J são **múltiplos de 4** (mais estrito que o RV32I, que admite 2), porque não há instruções
  comprimidas. Em consequência a faixa de B é −4096..4092 e a de J é −1048576..1048572.
- `SLL`/`SRL` são por registrador (as 19 do guia não incluem `SLLI`/`SRLI`); quantidade = `rs2[4:0]`.
- Nomes ABI (`a0`, `sp`...) não fazem parte da v1; só `x0`..`x31`.
- `LUI` guarda o valor do campo de 20 bits (0..0xFFFFF) em `imm`.
- Erros tipados (`InvalidRegisterError`, `ImmediateRangeError`, `UnsupportedInstructionError`, `FieldMismatchError`,
  `InvalidWordError`), todos `ValueError`.
- O mapa de E/S em `0xFFFF0000` foi a **premissa preliminar da dupla na Semana 07** e está superado; ele não é
  compatível com o mapa MMIO atual (`0x80000000`, `0x80000004`, `0x80000008`).

## 7. Coerência com as semanas anteriores

- `decoder.py` da Semana 01 foi **generalizado** (mesma API `decode`/`format_assembly`, mesmas saídas para ADD/ADDI);
  não existe segundo decodificador. Os testes das semanas 1 a 6 passam sem alteração.
- `scripts/measure_baseline.py` deixou de ter montadores locais e usa `encode` (o resultado versionado da Semana 02
  não muda: mesmas palavras).
- Na etapa da Semana 07, a CPU ainda executava só ADD/ADDI; o suporte de execução às 19 instruções foi concluído
  posteriormente e está refletido na documentação atual da arquitetura.
- O programa da Semana 01 usa `ecall`/`a7` para encerrar, o que está fora das 19 instruções; `soma.hex` não o usa.

## 8. Resultado da suíte

`pytest -q`: **574 testes, 574 aprovados** (251 anteriores + 323 desta semana). Sem regressões.

## 9. Estado do congelamento

O contrato está marcado **"v1 candidata a congelamento"**. O guia manda congelar *depois* da PR revisada; isso
exige a revisão cruzada da dupla e não foi simulado. Ao aprovar a PR, troque a linha de status do contrato por
`Status: v1 CONGELADA`.

## 10. Pendências (ação da dupla)

- Executar o simulador https://deniseribeiro-beep.github.io/faex-git-lab/isa-rv32i/ e salvar a exportação em
  `docs/semanas/Semana-07/vetores-simulador.json` (ou `.csv`). **Não foi feita** e o arquivo não foi inventado.
- Revisão cruzada da PR, congelar o contrato, tag `s07`, nomes e revisor acima.
