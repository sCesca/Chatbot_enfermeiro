import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from run import evaluate_symptoms, app
from typing import Generator
from flask import Flask

def test_evaluate_symptons() -> None:
    response: str = evaluate_symptoms("febre")
    assert "Você mencionou o sintoma: febre. Classificação: moderada." in response

    response = evaluate_symptoms("dor no peito")
    assert "Você mencionou o sintoma: dor no peito. Classificação: grave." in response

    response = evaluate_symptoms("dor de cabeça")
    assert "Você mencionou o sintoma: dor de cabeça. Classificação: leve." in response

    response = evaluate_symptoms("Sintoma desconhecido")
    assert "Desculpe, não entendi sua pergunta." in response

@pytest.fixture
def client() -> Generator[Flask, None, None]:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client