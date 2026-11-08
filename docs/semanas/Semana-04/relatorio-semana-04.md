# Relatório da Semana 04 - Lógica digital, MUX, decodificador e controle

- **Dupla:** _(preencher)_ · **Revisor da PR:** _(preencher)_ · **Branch:** `entrega/semana-04-logica-digital`

## 1. O que foi especificado, implementado e testado

| Bloco | Especificação | Implementação | Teste |
| --- | --- | --- | --- |
| AND, OR, NOT, XOR (+ SOP do XOR) | `docs/logica/tabelas-verdade.md` | `minirv/combinacional/gates.py` | `tests/test_gates.py` |
| MUX 2:1 | idem | `minirv/combinacional/mux.py` | `tests/test_mux.py` |
| Decodificador 2→4 | idem | `minirv/combinacional/decoder.py` | `tests/test_decoder2to4.py` |
| Controle por opcode (R, I, LOAD, STORE, BRANCH) | `docs/logica/sinais-controle.md` | `minirv/combinacional/control.py` | `tests/test_control.py` |

Os testes de portas e de controle **leem as tabelas dos arquivos `.md`** e comparam com o código; se alguém
alterar uma tabela ou uma função, a suíte falha.

## 2. Resultado dos testes

`pytest -q`: **112 testes, 112 aprovados** (60 anteriores + 52 desta semana). Cada bloco que valida entrada
tem teste de entrada inválida (`2`, `-1`, `None`, `"0"`, `1.0`, `True` e, para o controle, opcodes fora do
subconjunto e não inteiros).

## 3. Decisões tomadas

- **Validação estrita de tipo.** Em Python `True == 1` e `1.0 in (0, 1)`; a validação `x not in (0, 1)` do
  exemplo do roteiro aceitaria `True` e `1.0` em silêncio. Os blocos usam `type(x) is int` e `x in (0, 1)`.
- **`decode_control` devolve cópia** do dicionário, para que quem chama não altere a tabela interna.
- **Nome do teste do decoder:** `tests/test_decoder2to4.py`, porque `tests/test_decoder.py` já testa o
  decodificador de instruções da Semana 01 (o roteiro aceita estrutura equivalente). Pelo mesmo motivo existem
  `minirv/decoder.py` (instruções) e `minirv/combinacional/decoder.py` (2→4), em pacotes diferentes.
- **`xor_sop`** foi adicionada a `gates.py` para que a derivação SOP do XOR seja executável e testada.
- Estrutura em `minirv/combinacional/` (e não `src/combinacional/`), conforme `ADR-001`.

## 4. Dificuldades encontradas

Nenhuma bloqueante. O único ponto de atenção foi a armadilha `True == 1` descrita acima.

## 5. Diagrama

`docs/arquitetura.md` foi atualizado marcando em azul os blocos combinacionais (decodificador, controle,
MUX e ULA) e em laranja os que têm estado. O processador completo não é desenhado nesta semana.

## 6. Pendências

Nomes e revisor (acima); PR revisada e tag `s04` no GitHub **somente após o merge**.
