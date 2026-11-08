# Semana 08: Consolidação e versão final

> Esta pasta é o **estado completo do projeto ao final da Semana 08** (conteúdo exato da tag local `s08`).
> Contém tudo das semanas anteriores mais o que foi feito nesta; arquivos alterados aparecem aqui na versão mais recente.

## 1. Objetivo da semana

Consolidar: validar em clone limpo, registrar a regressão de desempenho, fechar a documentação e a matriz de requisitos. Não há documento oficial da Semana 8; esta etapa seguiu o roteiro de consolidação do pedido.

## 2. O que foi desenvolvido

- Validação em clone limpo com ambiente virtual novo.
- Seção 12 no relatório de desempenho: regressão de ~42% do decodificador novo, medida e justificada.
- README final, checklist de entrega, guia de publicação, arquitetura atualizada e matriz de requisitos final.

## 3. Arquivos criados nesta semana (3)

- `benchmarks/baseline/comparacao-s06-s08.json`: Comparação lado a lado do desempenho antes/depois do decodificador da Semana 07.
- `docs/checklist-final.md`: Checklist final de entrega: testes, status dos requisitos, pendências e lacunas.
- `docs/entrega-github.md`: Como publicar no GitHub (uma PR por semana ou repositório novo).

## 4. Arquivos modificados nesta semana (5)

- `PROJECT_PROGRESS.md`: Registro de andamento por semana (o que foi testado, implementado e o que está pendente).
- `README.md`: Apresentação do projeto: problema, objetivo, ferramentas, como executar, estrutura e divisão de responsabilidades.
- `docs/arquitetura.md`: Diagrama (Mermaid) da arquitetura e mapa bloco → módulo.
- `docs/matriz-requisitos.md`: Matriz de requisitos por semana, com status e evidência.
- `docs/semanas/Semana-02/orcamento-de-desempenho.md`: Relatório de desempenho e orçamento (11 seções; seção 12 acrescentada na Semana 08).

## 5. Funcionalidades já disponíveis neste estágio

- Tudo da Semana 7, validado em clone limpo.
- Documentação final, matriz de requisitos e checklist de entrega.

## 6. O que ainda NÃO existe neste estágio

Continua sem existir: montador de Assembly e execução das 19 instruções (dependem do documento da Semana 8). Dependem da dupla: PRs revisadas, tags no GitHub e evidências dos simuladores web.

## 7. Como executar e testar esta versão

```bash
cd Semana_08
python -m pip install -r requirements.txt
python -m pytest -q
python -m minirv.cpu programs/soma.hex
python -m minirv.executor --trace trace.json
python scripts/measure_baseline.py
```

Observação: `python -m pytest -q` deve ser executado **dentro** desta pasta (o `pytest.ini` já configura o caminho).

## 8. Resultado esperado ao final da semana

`pytest`: **574 passed in 1.42s** (medido ao gerar este pacote, executando os testes dentro desta pasta) com o capstone instalado; sem ele (`requirements-dev.txt` é opcional) são 531 aprovados e 1 ignorado.
Arquivos versionados nesta versão: **83** (3 novos, 5 modificados em relação à semana anterior).

## 9. Navegação

Anterior: `../Semana_07`. Esta é a versão final, idêntica ao projeto original.
Instruções Git desta etapa: `GITHUB_SEMANA_08.md`.
