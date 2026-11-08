# Semana 04: Lógica combinacional: portas, MUX, decoder e controle

> Esta pasta é o **estado completo do projeto ao final da Semana 04** (conteúdo exato da tag local `s04`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Construir e especificar os blocos de lógica combinacional: portas, MUX 2:1, decoder 2→4 e controle por classe de opcode (Atividade Semana 4).

## 2. O que foi desenvolvido

- Portas, MUX 2:1, decoder 2→4 e `decode_control` em `minirv/combinacional/`.
- Tabelas-verdade e sinais de controle documentados; os testes comparam o código com essas tabelas.
- Diagrama de arquitetura com blocos combinacionais marcados.

## 3. Arquivos criados nesta semana (12)

- `docs/logica/sinais-controle.md`: Tabela de sinais de controle por instrução (especificação do `control.py`).
- `docs/logica/tabelas-verdade.md`: Tabelas-verdade de AND/OR/XOR/NOT, MUX e decoder, e derivação SOP do XOR.
- `docs/semanas/Semana-04/relatorio-semana-04.md`: Relatório da Semana 04 (blocos combinacionais e decisões).
- `minirv/combinacional/__init__.py`: Marca o subpacote de lógica combinacional.
- `minirv/combinacional/control.py`: `decode_control(opcode)`: sinais de controle por classe (R, I, LOAD, STORE, BRANCH).
- `minirv/combinacional/decoder.py`: Decodificador 2→4 (uma e somente uma saída ativa).
- `minirv/combinacional/gates.py`: Portas AND, OR, NOT, XOR com validação estrita de bits e `xor_sop`.
- `minirv/combinacional/mux.py`: Multiplexador 2:1 com validação do seletor.
- `tests/test_control.py`: Testes do controle; compara o código com `sinais-controle.md`.
- `tests/test_decoder2to4.py`: Testes do decoder 2→4.
- `tests/test_gates.py`: Testes das portas lógicas e da tabela-verdade documentada.
- `tests/test_mux.py`: Testes do MUX 2:1.

## 4. Arquivos modificados nesta semana (3)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `docs/arquitetura.md`: Diagrama (Mermaid) da arquitetura e mapa bloco → módulo.
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 3.
- Portas, MUX, decoder 2→4 e sinais de controle por classe.

## 6. O que ainda NÃO existe neste estágio

Ainda não existem ALU completa, `read2`/`enable`, PC, memórias, executor nem contrato RV32I. Os blocos combinacionais ainda não estão ligados à CPU.

## 7. Como executar e testar esta versão

```bash
cd Semana_04
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.cpu programs/soma.hex
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **112 passed in 0.32s** (medido ao gerar este pacote, executando os testes dentro desta pasta).
Arquivos versionados nesta versão: **46** (12 novos, 3 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_03`. Próxima: `../Semana_05`.
Instruções Git desta etapa: `GITHUB_SEMANA_04.md`.
