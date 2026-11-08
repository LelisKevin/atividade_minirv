# Semana 03: Representação de 32 bits (word32)

> Esta pasta é o **estado completo do projeto ao final da Semana 03** (conteúdo exato da tag local `s03`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Implementar a representação de palavra de 32 bits (`word32`) e passar a reutilizá-la nos módulos existentes; organizar as pastas previstas (Laboratório 03).

## 2. O que foi desenvolvido

- `word32` (normalização, signed/unsigned, hex, binário, extensão de sinal, soma com overflow).
- `registers`, `alu`, `cpu`, `decoder` e `trace` passaram a reutilizar `word32` (sem máscara duplicada).
- ADR-001 resolvendo contradições entre os roteiros; pastas `workloads/` e `evidencias/`.

## 3. Arquivos criados nesta semana (6)

- `docs/adr/ADR-001-organizacao-do-repositorio-e-da-memoria.md`: Decisão: pasta `minirv/` em vez de `src/`, repositório e organização da memória (status Proposto).
- `docs/semanas/Semana-03/relatorio-semana-03.md`: Relatório da Semana 03 (máscara, overflow, casos-limite).
- `evidencias/README.md`: Pasta para evidências externas ao código (exportações de simuladores, capturas).
- `minirv/word32.py`: Representação de 32 bits: normalizar, unsigned/signed, hex, binário, extensão de sinal, soma.
- `tests/test_word32.py`: Testes do módulo word32 e casos-limite.
- `workloads/control/README.md`: Pasta da carga de controle; aponta para os arquivos da Semana 07.

## 4. Arquivos modificados nesta semana (8)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `README.md`: Apresentação do projeto: problema, objetivo, ferramentas, como executar, estrutura e divisão de responsabilidades.
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.
- `minirv/alu.py`: ULA de 32 bits (Sem. 1: ADD; Sem. 5: ADD, SUB, AND, OR, XOR, SLT, SLL, SRL).
- `minirv/cpu.py`: CPU mínima que executa ADD/ADDI, instrução por instrução ou contínua, com trace e CLI.
- `minirv/decoder.py`: Decodificador de instruções (Sem. 1: ADD/ADDI; Sem. 7: 19 instruções lidas do contrato).
- `minirv/registers.py`: Banco de registradores x0–x31 (x0 imutável; Sem. 5: `read2` e `write(enable)`).
- `minirv/trace.py`: Estrutura de trace e serialização JSON.

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 2.
- Conversões e normalização de 32 bits (`word32`).

## 6. O que ainda NÃO existe neste estágio

Ainda não existem lógica combinacional, ALU completa, banco com `read2`, PC, memórias, executor nem contrato RV32I.

## 7. Como executar e testar esta versão

```bash
cd Semana_03
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.cpu programs/soma.hex
python scripts/measure_baseline.py
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **60 passed in 0.26s** (medido ao gerar este pacote, executando os testes dentro desta pasta).
Arquivos versionados nesta versão: **34** (6 novos, 8 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_02`. Próxima: `../Semana_04`.
Instruções Git desta etapa: `GITHUB_SEMANA_03.md`.
