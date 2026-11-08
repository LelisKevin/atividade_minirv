# Simulação sequencial (Semana 05) — registro de previsões e resultados

Simulador da aula: https://deniseribeiro-beep.github.io/faex-git-lab/flipflops/

> **Estado deste arquivo.** As *previsões* (coluna 3) foram escritas a partir da teoria e ainda **não foram
> confrontadas com o simulador da aula**: essa execução é manual e está **pendente — ação da dupla**
> (coluna 4). A coluna 5 mostra o que o **código do projeto** produz (executado de verdade) nos dois
> experimentos em que o projeto tem componente equivalente (registrador e PC); latches e flip-flop não
> existem como módulos do MiniRV (o registrador é modelado como valor + `enable`).

| # | Experimento | Previsão (teoria) | Resultado no simulador da aula | Resultado no código do projeto |
| --- | --- | --- | --- | --- |
| 1 | SR latch em HOLD (S=0, R=0) | Q mantém o valor anterior (se Q=1 continua 1; se Q=0 continua 0); a latch "lembra". | _PENDENTE — ação da dupla_ | n/a (sem módulo) |
| 2 | D latch em HOLD (EN=0) | Q ignora D enquanto EN=0 e mantém o último valor capturado; com EN=1 (transparente) Q acompanha D. | _PENDENTE — ação da dupla_ | n/a (sem módulo) |
| 3 | D flip-flop em borda de subida | Q só assume D na transição CLK 0→1; mudanças de D entre as bordas não afetam Q. | _PENDENTE — ação da dupla_ | n/a (sem módulo) |
| 4 | Registrador com LOAD | Com LOAD=1 na borda, grava o valor; com LOAD=0 mantém. | _PENDENTE — ação da dupla_ | `write(3, 0xAB)`; `write(3, 0xCD, enable=False)` → x3 = 0x000000AB; `write(3, 0xCD, enable=True)` → x3 = 0x000000CD |
| 5 | PC com avanço/salto/reset | reset → 0; advance → +4; jump(0x100) → 0x100; advance → 0x104; reset → 0. | _PENDENTE — ação da dupla_ | 0x00000000 → 0x00000004 → 0x00000008 → 0x00000100 → 0x00000104 → 0x00000000 |

## Como completar

1. Abra o simulador, execute cada experimento e preencha a coluna 4 com o que realmente aconteceu.
2. Se algum resultado divergir da previsão, **não altere a previsão**: registre a divergência e a explicação.
3. Esta evidência complementa, mas não substitui, os entregáveis obrigatórios da Semana 05.

Ligação com o código: o experimento 4 é testado em `tests/test_registers.py`
(`test_enable_false_mantem_valor_anterior`) e o 5 em `tests/test_pc.py` (`test_sequencia_do_guia`).
