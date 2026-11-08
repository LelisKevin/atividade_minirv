# Relatório da Semana 05 - ALU, banco de registradores e estado sequencial

- **Dupla:** _(preencher)_ · **Revisor da PR:** _(preencher)_ · **Branch:** `entrega/semana-05-blocos-funcionais`
- **Valor:** 9 pontos

## 1. Objetivo e pergunta PBL

Criar blocos funcionais e avaliar invariantes do estado sequencial.
**Pergunta:** como combinar blocos funcionais para executar operações sem violar as regras de estado do processador?

## 2. Invariantes adotadas (definidas antes do código) e como cada uma foi testada

| # | Invariante | Teste |
| --- | --- | --- |
| I1 | Todos os resultados arquiteturais permanecem em 32 bits | `test_resultado_sempre_em_32_bits`, `test_entradas_sao_normalizadas_para_32_bits`, `test_escrever_x5_e_ler_valor_normalizado` |
| I2 | x0 retorna 0 em qualquer leitura e ignora qualquer escrita | `test_x0_apos_inicializacao_e_escrita_de_123`, `test_escrita_em_x0_com_enable_tambem_ignorada`, `test_sequencia_x1_x2_add_x3` |
| I3 | A ALU é combinacional (mesmas entradas, mesma saída; sem estado global) | `test_alu_e_combinacional` |
| I4 | O PC tem 32 bits e avança 4 bytes | `test_sequencia_do_guia`, `test_avanco_limitado_a_32_bits` |
| I5 | Reset leva o PC ao estado inicial | `test_sequencia_do_guia`, `test_reset_volta_ao_valor_inicial_configurado` |
| I6 | Entradas inválidas geram erro explícito | `test_operacao_invalida`, `test_operando_nao_inteiro`, `test_indice_fora_de_0_31_em_todas_as_operacoes`, `test_jump_invalido_gera_erro_e_preserva_estado` |

## 3. Módulos implementados

- `minirv/alu.py`: `execute(op, a, b)` com ADD, SUB, AND, OR, XOR, SLT, SLL, SRL; operação desconhecida gera `ValueError`.
- `minirv/registers.py`: 32 registradores, `read2(rs1, rs2)`, `write(rd, value, enable=True)`; `rd` é validado mesmo com `enable=False`.
- `minirv/pc.py`: `ProgramCounter` com `value`, `advance` (+4), `jump` (valida inteiro, 32 bits e alinhamento) e `reset`.
- `minirv/cpu.py` passou a usar `ProgramCounter` (o PC deixou de ser um inteiro solto dentro da CPU).

## 4. Cobertura da ALU

| Operação | Casos normais | Limites | Negativos | Overflow |
| --- | --- | --- | --- | --- |
| ADD | 5+7, 0+0 | 0x7FFFFFFF+1 | -1+5, -1+-1 | 0xFFFFFFFF+1 = 0 |
| SUB | 7-5, 5-5 | mínimo-1 = 0x7FFFFFFF | -3-(-5) | 0-1 = 0xFFFFFFFF |
| AND | padrões alternados | x & 0 | — | — |
| OR | 0 \| valor, padrões complementares | — | — | — |
| XOR | v ^ v = 0, padrões diferentes | — | — | — |
| SLT | menor, maior, igual | 0x80000000 < 0x7FFFFFFF | -1 < 1 (com sinal) | — |
| SLL | desloc. 0 e 1 | 31 e 32 (32 → 0) | — | perda de bits (3 << 31) |
| SRL | desloc. 0 e 1 | 0x80000000 >> 31 e >> 32 | MSB=1 sem propagar sinal | — |

**Limite de deslocamento adotado pelo contrato:** apenas os 5 bits menos significativos de `b` valem
(0 a 31); deslocar por 32 equivale a deslocar por 0, como no RV32I.

## 5. Evidência do x0 imutável

`write(0, 123)` e `write(0, v, enable=True)` mantêm x0 = 0; na sequência `x1=5, x2=7, x3=12`, x0 continua 0 ao
final (`tests/test_sequencia.py`). A CPU da Semana 01 também não registra escrita em x0 no trace.

## 6. Sequência de testes do PC

reset → `0x00000000` · advance → `0x00000004` · advance → `0x00000008` · jump(0x100) → `0x00000100` ·
advance → `0x00000104` · reset → `0x00000000` (`tests/test_pc.py::test_sequencia_do_guia`).
Desvios por composição: BEQ (via `SUB == 0`), BNE e BLT com sinal (via `SLT == 1`) decidem entre `advance` e `jump`.

## 7. Sequência leitura → cálculo → escrita

Estado inicial (tudo 0) → escrever x1=5 → escrever x2=7 → ler x1, x2 → ALU ADD = 12 → escrever x3=12 →
estado final: x0=0, x1=5, x2=7, x3=12. A leitura e o cálculo não alteram registradores, e a execução repetida
produz o mesmo log (`tests/test_sequencia.py`).

## 8. Resultado da suíte

`pytest -q`: **204 testes, 204 aprovados** (112 das semanas anteriores já incluídos; 92 novos ou ampliados nesta semana).

## 9. Referência à simulação sequencial

`docs/semanas/Semana-05/simulacao-sequencial.md` (previsões e resultados do projeto preenchidos; resultados do
simulador da aula **pendentes**).

## 10. Limitações e pendências para a Semana 06

- ALU, registradores e PC ainda não estão integrados em um ciclo completo (Semana 06).
- O PC aceita apenas alvos múltiplos de 4 (não há instruções comprimidas); o RV32I permite alvos pares, mas o
  contrato do MiniRV adota múltiplos de 4 (registrado na Semana 07).
- Pendente (ação da dupla): executar o simulador de flip-flops, nomes e revisor, PR revisada e tag `s05`.
