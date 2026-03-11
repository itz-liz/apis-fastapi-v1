import requests
import pytest

URL_BASE = "http://localhost:8000"


def test_read_root():
    url = f"{URL_BASE}/"
    response = requests.get(url)
    assert response.status_code == 202
    assert response.json()["message"] == "API de la agenda"


@pytest.mark.parametrize(
    "params,status,message",
    [
        ({}, 400, "limit y skip no pueden ser nulos"),
        ({"skip": "1"}, 400, "limit no puede ser nulo"),
        ({"limit": "1"}, 400, "skip no puede ser nulo"),
        ({"limit": "abc", "skip": "xyz"}, 400, "limit y skip no pueden ser un conjunto de letras"),
        ({"limit": "abc", "skip": "1"}, 400, "limit no puede ser un string"),
        ({"limit": "1", "skip": "abc"}, 400, "skip no puede ser un string"),
        ({"limit": "-1", "skip": "-1"}, 400, "limit y skip no pueden ser negativos"),
        ({"limit": "-1", "skip": "1"}, 400, "limit no puede ser negativo"),
        ({"limit": "1", "skip": "-1"}, 400, "skip no puede ser negativo"),
        ({"limit": "0", "skip": "1"}, 407, "limit no puede ser cero"),
        ({"limit": "1", "skip": "0"}, 407, "skip no puede ser cero"),
    ],
)
def test_get_contactos_limitskip_validaciones(params, status, message):
    url = f"{URL_BASE}/v1/contactos"
    response = requests.get(url, params=params)
    assert response.status_code == status
    assert response.json()["message"] == message