# Semana 01: Estrutura inicial e primeiro programa

> Esta pasta é o **estado completo do projeto ao final da Semana 01** (conteúdo exato da tag local `s01`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Criar a estrutura do repositório, entender o produto e entregar a primeira versão mínima: ler instruções hexadecimais, executar `ADDI`/`ADD`, alterar registradores e gerar um trace JSON (How To Semana 1).

## 2. O que foi desenvolvido

- Registradores x0–x31 com x0 imutável, ULA com ADD, decodificador de ADD/ADDI, CPU mínima (passo a passo e contínua) e trace JSON.
- Programa `soma.hex` (5 + 7 = 12) e testes de ADD e de x0 = 0.

## 3. Arquivos criados nesta semana (19)

- `.gitignore`: Ignora venv, caches e arquivos de editor.
- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `README.md`: Apresentação do projeto: problema, objetivo, ferramentas, como executar, estrutura e divisão de responsabilidades.
- `docs/arquitetura.md`: Diagrama (Mermaid) da arquitetura e mapa bloco → módulo.
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.
- `minirv/__init__.py`: Marca `minirv` como pacote Python.
- `minirv/alu.py`: ULA de 32 bits (Sem. 1: ADD; Sem. 5: ADD, SUB, AND, OR, XOR, SLT, SLL, SRL).
- `minirv/cpu.py`: CPU mínima que executa ADD/ADDI, instrução por instrução ou contínua, com trace e CLI.
- `minirv/decoder.py`: Decodificador de instruções (Sem. 1: ADD/ADDI; Sem. 7: 19 instruções lidas do contrato).
- `minirv/registers.py`: Banco de registradores x0–x31 (x0 imutável; Sem. 5: `read2` e `write(enable)`).
- `minirv/trace.py`: Estrutura de trace e serialização JSON.
- `programs/soma.hex`: Programa de 3 palavras RV32I reais: soma 5 + 7 em x3.
- `programs/soma.s`: Assembly de referência do programa soma (para conferir no RARS).
- `pytest.ini`: Configuração do pytest (testpaths e `pythonpath = .`).
- `requirements.txt`: Dependência de execução/testes (pytest).
- `tests/test_alu.py`: Testes da ALU (casos normais, limites, negativos e overflow).
- `tests/test_cpu.py`: Testes da CPU: soma, trace, x0, passo a passo e linha de comando.
- `tests/test_decoder.py`: Testes do decodificador de instruções.
- `tests/test_registers.py`: Testes do banco de registradores (x0 imutável, read2, enable, índices inválidos).

## 4. Arquivos modificados nesta semana (0)

_(nenhum)_

## 5. Funcionalidades já disponíveis neste estágio

- Executar `programs/soma.hex` e obter x3 = 12 com trace JSON.
- Execução passo a passo (`--step`) e contínua.

## 6. O que ainda NÃO existe neste estágio

Não há word32, ALU além de ADD, PC como módulo, memórias, lógica combinacional, benchmark, nem contrato da ISA. A CPU só conhece `ADD` e `ADDI` e não tem memória de dados.

## 7. Como executar e testar esta versão

```bash
cd Semana_01
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.cpu programs/soma.hex
python -m minirv.cpu programs/soma.hex --step
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **26 passed in 0.12s** (medido ao gerar este pacote, executando os testes dentro desta pasta).
Arquivos versionados nesta versão: **19** (19 novos, 0 modificados em relação à semana anterior).

## 9. Navegação

Primeira versão. Próxima: `../Semana_02`.
Instruções Git desta etapa: `GITHUB_SEMANA_01.md`.
