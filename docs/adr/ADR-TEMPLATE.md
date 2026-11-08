# ADR-XXX - Alteração no contrato da ISA

Status: Proposto | Aceito | Rejeitado

Contexto:
(Qual problema ou necessidade motiva a mudança? Qual instrução, sintaxe, codificação ou semântica do
`docs/isa/rv32i-subset-v1.md` é afetada?)

Decisão:
(O que será mudado, e por que as alternativas foram descartadas.)

Impacto em encode/decode:
(`minirv/encoder.py`, `minirv/decoder.py`; a tabela do contrato é lida por `minirv/isa.py`.)

Impacto em testes:
(Vetores de `tests/vectors/`, testes negativos, ida e volta, módulos das semanas anteriores.)

Impacto no Assembly:
(Sintaxe, montador da Semana 08, programas existentes como `controlador-preliminar.s`.)

---
Regra: depois do congelamento da v1, nenhuma instrução, sintaxe, codificação ou semântica muda sem um ADR
aceito. Numerar em sequência (`ADR-003`, `ADR-004`...) e referenciar a PR da mudança.
