# Semana 07: Contrato RV32I v1: encode/decode e vetores

> Esta pasta é o **estado completo do projeto ao final da Semana 07** (conteúdo exato da tag local `s07`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Congelar a versão 1 do contrato do subconjunto RV32I: especificação, encode/decode, vetores e programa Assembly preliminar (Atividade Semana 7).

## 2. O que foi desenvolvido

- Contrato RV32I v1 (19 instruções, 6 layouts, sintaxe, erros, regularidade) em `docs/isa/rv32i-subset-v1.md`.
- `isa.py` lê o contrato; `encoder.py` e o `decoder.py` generalizado usam a mesma especificação.
- 43 vetores válidos, 43 negativos, propriedade encode → decode, conferência com o capstone; programa preliminar e mapeamento da carga.
- `scripts/measure_baseline.py` passou a usar `encode`; a CPU recusa com erro explícito instruções que decodifica mas não executa.

## 3. Arquivos criados nesta semana (16)

- `docs/adr/ADR-TEMPLATE.md`: Modelo de ADR para mudanças futuras no contrato da ISA.
- `docs/isa/rv32i-subset-v1.md`: Contrato do subconjunto RV32I v1: 19 instruções, 6 layouts, sintaxe, erros e regularidade (fonte única lida por `isa.py`).
- `docs/semanas/Semana-07/controlador-preliminar.s`: Programa Assembly preliminar do controlador térmico (leitura, decisão, estado, escrita, laço); não executado.
- `docs/semanas/Semana-07/mapeamento-carga-isa.md`: Mapeamento das necessidades da carga canônica para instruções do contrato.
- `docs/semanas/Semana-07/relatorio-semana-07.md`: Relatório da Semana 07 (vetores, verificações, decisões, pendências).
- `minirv/encoder.py`: `encode`: instrução estruturada → palavra de 32 bits, conforme o contrato.
- `minirv/isa.py`: Lê a tabela do contrato `.md` como especificação única e define os erros tipados da ISA.
- `requirements-dev.txt`: Dependência opcional (capstone) para a validação independente das codificações RV32I.
- `tests/test_controlador_preliminar.py`: Confere o programa preliminar contra o contrato (sintaxe, faixas, rótulos, cobertura).
- `tests/test_isa_capstone.py`: Validação independente dos vetores com o capstone (ignorado se não instalado).
- `tests/test_isa_contrato.py`: Testes do contrato: 19 instruções, codificações do manual RISC-V, layouts, leitura rigorosa.
- `tests/test_isa_negativos.py`: Casos negativos: registrador, imediato, opcode/funct, campos.
- `tests/test_isa_roundtrip.py`: Propriedade encode → decode (aleatória, limites e 200.000 palavras).
- `tests/test_isa_vetores.py`: Vetores válidos: palavra produzida, volta por decode e sintaxe canônica.
- `tests/vectors/rv32i-v1-negativos.json`: 43 casos negativos de encode/decode (dados dos testes).
- `tests/vectors/rv32i-v1.json`: 43 vetores válidos (assembly, palavra e campos esperados).

## 4. Arquivos modificados nesta semana (6)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.
- `minirv/cpu.py`: CPU mínima que executa ADD/ADDI, instrução por instrução ou contínua, com trace e CLI.
- `minirv/decoder.py`: Decodificador de instruções (Sem. 1: ADD/ADDI; Sem. 7: 19 instruções lidas do contrato).
- `scripts/measure_baseline.py`: Coletor de métricas de desempenho com verificação de orçamento.
- `tests/test_cpu.py`: Testes da CPU: soma, trace, x0, passo a passo e linha de comando.

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 6.
- `encode`/`decode` das 19 instruções RV32I a partir do contrato; vetores e propriedade de ida e volta.

## 6. O que ainda NÃO existe neste estágio

Não existem montador de Assembly nem execução das 19 instruções (a CPU decodifica todas mas executa só ADD/ADDI). O contrato ainda está como candidato a congelamento.

## 7. Como executar e testar esta versão

```bash
cd Semana_07
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.executor --trace trace.json
# opcional: python -m pip install -r requirements-dev.txt  (habilita o teste do capstone)
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **574 passed in 1.10s** (medido ao gerar este pacote, executando os testes dentro desta pasta) com o capstone instalado; sem ele (`requirements-dev.txt` é opcional) são 531 aprovados e 1 ignorado.
Arquivos versionados nesta versão: **80** (16 novos, 6 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_06`. Próxima: `../Semana_08`.
Instruções Git desta etapa: `GITHUB_SEMANA_07.md`.
