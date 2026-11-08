# Relatório da Semana 03 - Representação de dados em 32 bits

- **Dupla:** _(preencher)_ · **Data:** _(preencher)_ · **Revisor da PR:** _(preencher)_
- **Branch:** `entrega/semana-03-word32`

## 1. Objetivo da semana

Implementar o módulo `minirv/word32.py`, que normaliza, converte e interpreta palavras de 32 bits,
e testar os casos-limite e o overflow. O módulo é o primeiro componente técnico do simulador e passa a
ser reutilizado por registradores, ULA, decodificador e trace (nenhum deles repete a máscara).

## 2. A máscara 0xFFFFFFFF

O Python aceita inteiros de qualquer tamanho; o simulador não pode depender disso. `normalizar32(v)` calcula
`v & 0xFFFFFFFF`, preservando só os 32 bits menos significativos. Para números negativos, o `&` do Python
opera sobre a representação em complemento de dois de precisão infinita, então `-1 & 0xFFFFFFFF = 0xFFFFFFFF`.

## 3. Overflow em 32 bits

Após uma operação, mantêm-se apenas os 32 bits que cabem na palavra. `0xFFFFFFFF + 1 = 0x100000000`
(33 bits) e a normalização descarta o bit 32, resultando em `0x00000000`. O mesmo padrão de bits tem
duas leituras: `0xFFFFFFFF` é 4.294.967.295 em unsigned e −1 em signed. `0x7FFFFFFF + 1` vira `0x80000000`,
que em signed é −2.147.483.648 (overflow com sinal).

## 4. Casos-limite

| Caso | Entrada | Hex | Unsigned | Signed | Binário (32 bits) |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0x00000000 | 0 | 0 | `00000000000000000000000000000000` |
| −1 | -1 | 0xFFFFFFFF | 4294967295 | -1 | `11111111111111111111111111111111` |
| 2³¹ − 1 | 2147483647 | 0x7FFFFFFF | 2147483647 | 2147483647 | `01111111111111111111111111111111` |
| −2³¹ | -2147483648 | 0x80000000 | 2147483648 | -2147483648 | `10000000000000000000000000000000` |
| 0xFFFFFFFF + 1 | 0x100000000 | 0x00000000 | 0 | 0 | `00000000000000000000000000000000` |
| 0x2A | 42 | 0x0000002A | 42 | 42 | `00000000000000000000000000101010` |

(tabela gerada chamando o próprio `word32`, não digitada)

## 5. Operações do módulo

`normalizar32`, `para_unsigned32`, `para_signed32`, `para_hex32` (8 dígitos + `0x`), `para_bin32` (sempre 32
dígitos), `estender_sinal(valor, bits_origem)` e `soma32`. Entradas não inteiras (incluindo `bool`) e
`bits_origem` fora de 1..32 geram `ValueError`.

## 6. Resultado dos testes

`pytest -q`: **60 testes, 60 aprovados** (26 da Semana 01 + 7 da Semana 02 + 27 desta semana). Os testes
novos estão em `tests/test_word32.py` e cobrem os seis casos-limite do roteiro, extensão de sinal de 12 bits
(imediato do RISC-V), entradas inválidas e a normalização na escrita de registradores.

## 7. Decisões e pontos em que o roteiro conflita com o projeto

Resolvidos em [`ADR-001`](../../adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md): pasta `minirv/` em vez de
`src/`, nome do repositório e organização da memória.

## 8. Pendências

- Nomes, data e revisor (acima).
- PR revisada e tag `s03` no GitHub, após o merge.
