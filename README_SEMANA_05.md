# Semana 05: ALU, banco de registradores e PC

> Esta pasta é o **estado completo do projeto ao final da Semana 05** (conteúdo exato da tag local `s05`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Criar a ALU completa, o banco de 32 registradores com invariante x0 = 0 e o Program Counter (Atividade Semana 5).

## 2. O que foi desenvolvido

- ALU com 8 operações; `RegisterFile` com `read2` e `write(enable)`; `ProgramCounter`.
- Desvios testados por composição (BEQ/BNE/BLT); sequência x1=5, x2=7, x3=12; mapa operação → sinal.
- A CPU passou a usar `ProgramCounter` em vez de um inteiro solto.

## 3. Arquivos criados nesta semana (6)

- `docs/semanas/Semana-05/mapa-operacoes.md`: Mapa operação → entrada → saída → sinal, gerado executando os componentes.
- `docs/semanas/Semana-05/relatorio-semana-05.md`: Relatório da Semana 05 (invariantes ↔ testes, cobertura da ALU).
- `docs/semanas/Semana-05/simulacao-sequencial.md`: Previsões e resultados dos 5 experimentos sequenciais (resultados do simulador web pendentes).
- `minirv/pc.py`: Program Counter de 32 bits: avanço de 4, salto validado e reset.
- `tests/test_pc.py`: Testes do PC e dos desvios por composição.
- `tests/test_sequencia.py`: Sequência leitura → cálculo → escrita (x1=5, x2=7, x3=12).

## 4. Arquivos modificados nesta semana (7)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.
- `minirv/alu.py`: ULA de 32 bits (Sem. 1: ADD; Sem. 5: ADD, SUB, AND, OR, XOR, SLT, SLL, SRL).
- `minirv/cpu.py`: CPU mínima que executa ADD/ADDI, instrução por instrução ou contínua, com trace e CLI.
- `minirv/registers.py`: Banco de registradores x0–x31 (x0 imutável; Sem. 5: `read2` e `write(enable)`).
- `tests/test_alu.py`: Testes da ALU (casos normais, limites, negativos e overflow).
- `tests/test_registers.py`: Testes do banco de registradores (x0 imutável, read2, enable, índices inválidos).

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 4.
- ALU de 8 operações, banco de registradores completo, PC com avanço/salto/reset.

## 6. O que ainda NÃO existe neste estágio

Ainda não existem memórias, executor do ciclo de 5 estados nem contrato RV32I; a ALU, os registradores e o PC ainda não formam um ciclo completo.

## 7. Como executar e testar esta versão

```bash
cd Semana_05
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.cpu programs/soma.hex
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **204 passed in 0.39s** (medido ao gerar este pacote, executando os testes dentro desta pasta).
Arquivos versionados nesta versão: **52** (6 novos, 7 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_04`. Próxima: `../Semana_06`.
Instruções Git desta etapa: `GITHUB_SEMANA_05.md`.
