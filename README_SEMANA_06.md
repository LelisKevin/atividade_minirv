# Semana 06: Memórias e ciclo de instrução

> Esta pasta é o **estado completo do projeto ao final da Semana 06** (conteúdo exato da tag local `s06`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Criar as memórias de instruções e de dados e integrar o primeiro ciclo de instrução observável em cinco estados (Atividade Semana 6).

## 2. O que foi desenvolvido

- Memória de instruções e memória de dados (alinhamento, faixa, erro com endereço e causa).
- Executor de 5 estados (FETCH, DECODE, EXECUTE, MEMORY, WRITEBACK) com rastro; microssequência de 3 instruções controladas.
- Verificação manual, interfaces de barramento, diagrama do ciclo e rastro do projeto. `cpu.py` passou a usar `InstructionMemory`.

## 3. Arquivos criados nesta semana (12)

- `docs/semanas/Semana-06/diagrama-ciclo.md`: Diagramas Mermaid do ciclo de instrução e dos cinco estados.
- `docs/semanas/Semana-06/interfaces-barramento.md`: Tabela de interfaces entre blocos, com os nomes reais do código.
- `docs/semanas/Semana-06/relatorio-semana-06.md`: Relatório da Semana 06 com comparação manual × automático.
- `docs/semanas/Semana-06/trace-projeto.json`: Rastro arquitetural (15 eventos) gerado por `python -m minirv.executor`.
- `docs/semanas/Semana-06/verificacao-manual.md`: Verificação manual da microssequência de 3 instruções (escrita antes da execução).
- `minirv/data_memory.py`: Memória de dados por byte (little-endian) com validação de alinhamento e faixa.
- `minirv/executor.py`: Executor do ciclo de 5 estados (FETCH…WRITEBACK) com rastro, para as instruções controladas.
- `minirv/instruction_memory.py`: Memória de instruções somente leitura (`read_word`).
- `minirv/memory_access.py`: Validação de acesso compartilhada pelas memórias (`MemoryAccessError`).
- `tests/test_data_memory.py`: Testes de alinhamento, faixa, mensagens de erro e ausência de escrita parcial.
- `tests/test_executor.py`: Testes do ciclo de 5 estados, rastro e estado final da microssequência.
- `tests/test_instruction_memory.py`: Testes da memória de instruções.

## 4. Arquivos modificados nesta semana (3)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.
- `minirv/cpu.py`: CPU mínima que executa ADD/ADDI, instrução por instrução ou contínua, com trace e CLI.

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 5.
- Memórias com validação, ciclo de 5 estados com rastro, microssequência x3=12, mem[0]=12, x4=12, PC=0x0000000C.

## 6. O que ainda NÃO existe neste estágio

Ainda não existem encode/decode das 19 instruções nem o contrato RV32I; o executor só roda 3 instruções didáticas (identificadores, não codificações RV32I).

## 7. Como executar e testar esta versão

```bash
cd Semana_06
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.executor --trace trace.json
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **251 passed in 0.67s** (medido ao gerar este pacote, executando os testes dentro desta pasta).
Arquivos versionados nesta versão: **64** (12 novos, 3 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_05`. Próxima: `../Semana_07`.
Instruções Git desta etapa: `GITHUB_SEMANA_06.md`.
