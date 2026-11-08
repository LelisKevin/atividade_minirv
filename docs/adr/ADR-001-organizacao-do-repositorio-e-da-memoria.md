# ADR-001 - Organização do repositório e da memória

Status: Proposto (a dupla confirma na revisão da PR da Semana 03; depois muda para Aceito)

## Contexto

Os roteiros semanais divergem em alguns pontos e a Semana 06 cita "a decisão de organização de memória
registrada na Semana 01", que o How To da Semana 01 não registra.

| Ponto | Semana 01 | Semanas 03 a 05 |
| --- | --- | --- |
| Pasta do código | pacote `minirv/` (`minirv/minirv/*.py` dentro do repositório) | `src/` |
| Nome do repositório | `minirv-dupla-01` | `ac-riscv-2026-dupla-N` |
| Criação do repositório | Semana 01 | repete "criar repositório" no Laboratório 03 |
| Organização da memória | não registrada | exigida como já decidida (Sem. 06) |

## Decisão

1. **Código em `minirv/`** (pacote Python), como fixado na Semana 01. Os caminhos `src/xxx.py` dos roteiros
   correspondem a `minirv/xxx.py`; os imports são `from minirv.xxx import ...`. As Semanas 04 e 05 admitem
   estrutura equivalente; manter uma só evita módulos duplicados.
2. **Repositório existente mantido** (`minirv-dupla-01`); o passo de criar repositório do Laboratório 03 é
   considerado cumprido na Semana 01.
3. **Organização da memória**, registrada aqui por falta de registro anterior:
   - endereçada por **byte**; palavra de 32 bits em **little-endian** (como no RV32I);
   - acessos de **palavra inteira**, alinhados em 4 bytes (sem `LB`/`SB`/`LH`/`SH` no subconjunto);
   - **memória de instruções e memória de dados separadas** (interfaces da Semana 06);
   - memória de dados com endereço base 0 e tamanho padrão de **4 KiB** (1.024 palavras), configurável no construtor;
   - PC de 32 bits, começa em 0 e avança de 4 em 4;
   - a região 0xFFFF0000 em diante é reservada para E/S mapeada em memória (usada no programa preliminar da
     Semana 07) e **não faz parte** da memória de dados nesta fase.
4. `word32` é o único lugar com a máscara de 32 bits.

## Consequências

- Imports uniformes em código, testes e scripts; roteiros futuros devem ser lidos com a substituição `src/` → `minirv/`.
- A memória de dados de 4 KiB limita a carga de trabalho; aumentar o tamanho não exige ADR (é parâmetro).
- O ADR deve ser revisto se a disciplina fixar outro tamanho ou outro mapa de E/S.

## Impacto

`minirv/data_memory.py` (Semana 06), `docs/semanas/Semana-07/controlador-preliminar.s`.
