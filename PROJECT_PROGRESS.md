# Progresso do projeto MiniRV

Registro do andamento real. Nada aqui é marcado como concluído sem ter sido executado.
Matriz completa: [`docs/matriz-requisitos.md`](docs/matriz-requisitos.md).

Legenda: **Testado e aprovado** · **Implementado** (sem teste automatizável) · **Pendente — ação sua**.

## Semana 1 — Estruturação (branch `feature/s01-nucleo-minimo`)

- Testado e aprovado: banco de registradores com x0 imutável, ULA (ADD), decodificador (ADD/ADDI), CPU mínima passo a passo/contínua, trace JSON, programa `soma.hex` (x3 = 12). 26 testes, 26 aprovados.
- Implementado: README, diagrama de arquitetura (Mermaid), `.gitignore`, `requirements.txt`, `pytest.ini`.
- Pendente — ação sua: criar repositório privado e adicionar a professora; abrir a Issue S01; PR revisada pelo colega; tag `s01` no GitHub; preencher nomes no README.
- Observação: o programa do guia usa `addi a7` + `ecall` para sair; `ecall` não pertence ao subconjunto, então `soma.hex` tem só as 3 instruções e a CPU encerra quando o PC passa do fim. O `.s` completo fica em `programs/soma.s` para o RARS.
