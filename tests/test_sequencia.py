"""Sequência leitura -> cálculo -> escrita (Semana 05, Passo 9). Determinística e repetível."""
from minirv.alu import execute
from minirv.registers import RegisterFile


def rodar_sequencia():
    r = RegisterFile()
    log = [("estado inicial", r.dump())]
    r.write(1, 5);  log.append(("escrever x1 = 5", r.dump()))
    r.write(2, 7);  log.append(("escrever x2 = 7", r.dump()))
    a, b = r.read2(1, 2); log.append((f"ler x1, x2 -> {a}, {b}", r.dump()))
    soma = execute("ADD", a, b); log.append((f"ALU ADD -> {soma}", r.dump()))
    r.write(3, soma);  log.append(("escrever x3 = 12", r.dump()))
    return r, log


def test_sequencia_x1_x2_add_x3():
    r, log = rodar_sequencia()
    assert r.read(0) == 0
    assert r.read(3) == 12
    assert (r.read(1), r.read(2)) == (5, 7)
    assert len(log) == 6
    assert log[0][1] == {f"x{i}": 0 for i in range(32)}  # estado inicial
    assert {k: v for k, v in log[-1][1].items() if v} == {"x1": 5, "x2": 7, "x3": 12}


def test_sequencia_e_deterministica():
    assert rodar_sequencia()[1] == rodar_sequencia()[1]


def test_leitura_nao_altera_estado_entre_passos():
    _, log = rodar_sequencia()
    assert log[2][1] == log[3][1] == log[4][1]  # ler e calcular não mudam registradores
