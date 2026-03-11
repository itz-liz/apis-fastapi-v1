import requests
import pytest
import time

URL_BASE = "http://localhost:8000"

# TODO: 0. GET 202 / Mensaje de bienvenida
def test_read_root():
    url = f"{URL_BASE}/"
    response = requests.get(url)
    data = {
        "message": "Api de la Agenda",
        "datatime": time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
        }
    assert response.status_code == 202
    assert response.json () == data

# TODO: 1. GET 202 /v1/contactos?limit=10&skip=0 primeros 10 contactos 
def test_get_contactos_limit_10_skip_0():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=0"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 202
    assert body["table"] == "contactos"
    assert body["message"] == "Datos consultados exitosamente"
    assert body["limit"] == 10
    assert body["skip"] == 0
    assert body["count"] == 10
    assert len(body["items"]) == 10
    for contacto in body["items"]:
        assert "id_contacto" in contacto
        assert "nombre" in contacto
        assert "telefono" in contacto
        assert "email" in contacto

# TODO: 2. GET 202 /v1/contactos?limit=10&skip=90 ultimos 10 contacto
def test_get_contactos_limit_10_skip_90():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=90"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 202
    assert body["table"] == "contactos"
    assert body["message"] == "Datos consultados exitosamente"
    assert body["limit"] == 10
    assert body["skip"] == 90
    assert body["count"] == len(body["items"])

# TODO: 3. GET 400 /v1/contactos?limit=-10&skip=0 Error en limit
def test_get_contactos_limit_negativo_skip_0():
    url = f"{URL_BASE}/v1/contactos?limit=-10&skip=0"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "limit no puede ser negativo"

# TODO: 4. GET 400 /v1/contactos?limit=10&skip=-10 Error en skip
def test_get_contactos_limit_10_skip_negativo():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=-10"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "skip no puede ser negativo"

# TODO: 5. GET 202 /v1/contactos?limit=0&skip=0 vacio
def test_get_contactos_limit_0_skip_0():
    url = f"{URL_BASE}/v1/contactos?limit=0&skip=0"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 202
    assert body["table"] == "contactos"
    assert body["items"] == []
    assert body["count"] == 0
    assert body["limit"] == 0
    assert body["skip"] == 0
    assert body["message"] == "Datos consultados exitosamente"

# TODO: 6. GET 202 /v1/contactos?skip=0 Regresar los primeros 10 contactos por default
def test_get_contactos_skip_0():
    url = f"{URL_BASE}/v1/contactos?skip=0"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 202
    assert body["limit"] == 10
    assert body["skip"] == 0
    assert body["count"] == 10
    assert body["message"] == "Datos consultados exitosamente"

# TODO: 7. GET 202 /v1/contactos?limit=10 Regresar los primeros 10 contactos por default
def test_get_contactos_limit_10():
    url = f"{URL_BASE}/v1/contactos?limit=10"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 202
    assert body["limit"] == 10
    assert body["skip"] == 0
    assert body["count"] == 10
    assert body["message"] == "Datos consultados exitosamente"

# TODO: 8. GET 202 /v1/contactos Regresar los primeros 10 contactos por default
def test_get_contactos():
    url = f"{URL_BASE}/v1/contactos"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 202
    assert body["limit"] == 10
    assert body["skip"] == 0
    assert body["count"] == 10
    assert body["message"] == "Datos consultados exitosamente"

# TODO: 9. GET 400 /v1/contactos?limit=x&skip=100 Mensaje de Error en limit
def test_get_contactos_limit_x_skip_100():
    url = f"{URL_BASE}/v1/contactos?limit=x&skip=100"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "limit no puede ser un string"

# TODO: 10. GET 400 /v1/contactos?limit=10&skip=x Mensaje de Error en skip
def test_get_contactos_limit_10_skip_x():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=x"
    response = requests.get(url)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "skip no puede ser un string"
