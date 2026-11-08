import json
from pathlib import Path

import pytest

from scripts import measure_baseline as mb

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "benchmarks/baseline/config.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def entrada_tmp(tmp_path_factory):
    p = tmp_path_factory.mktemp("bench") / "entrada.csv"
    mb.salvar_entrada(p, mb.gerar_entrada(100))
    return p


def test_entrada_e_deterministica():
    assert mb.gerar_entrada(1000) == mb.gerar_entrada(1000)
    assert all(15 <= t <= 35 for t in mb.gerar_entrada(1000))


def test_tres_repeticoes_com_campos_numericos_nao_negativos(entrada_tmp):
    res = mb.executar(CONFIG, entrada_path=entrada_tmp)
    assert len(res) == 3
    for r in res:
        for campo in ("tempo_decorrido_s", "memoria_pico_bytes", "tamanho_rastro_bytes"):
            assert isinstance(r[campo], (int, float)) and r[campo] >= 0


def test_saida_e_arquitetura_corretas(entrada_tmp):
    temps = mb.ler_entrada(entrada_tmp)
    r = mb.executar(CONFIG, entrada_path=entrada_tmp, repeticoes=1)[0]
    assert r["amostras"] == 100
    assert r["soma_temperaturas"] == sum(temps)
    arq = r["arquitetura"]
    assert arq["instrucoes_executadas"] == 200
    assert arq["ciclos_simulados"] == 200 * arq["cpi_modelado"]
    assert arq["tempo_modelado_s"] == pytest.approx(arq["ciclos_simulados"] / 100e6)


def test_repeticoes_sao_reproduziveis(entrada_tmp):
    a, b = mb.executar(CONFIG, entrada_path=entrada_tmp, repeticoes=2)
    assert a["soma_temperaturas"] == b["soma_temperaturas"]
    assert a["tamanho_rastro_bytes"] == b["tamanho_rastro_bytes"]


def test_orcamento_dentro_do_limite(entrada_tmp):
    assert mb.verificar_orcamento(mb.executar(CONFIG, entrada_path=entrada_tmp), CONFIG) == []


def test_orcamento_detecta_violacao():
    ruim = [{"tempo_decorrido_s": 9.0, "memoria_pico_bytes": 1, "tamanho_rastro_bytes": 1}] * 3
    assert any("tempo médio" in p for p in mb.verificar_orcamento(ruim, CONFIG))


def test_resultados_brutos_versionados_tem_tres_repeticoes():
    dados = json.loads((ROOT / "benchmarks/baseline/resultados-brutos.json").read_text(encoding="utf-8"))
    assert len(dados) == 3
    assert all("tempo_decorrido_s" in r and "memoria_pico_bytes" in r for r in dados)
