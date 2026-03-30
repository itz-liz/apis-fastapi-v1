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


def _crear_contacto_para_pruebas(nombre: str = "Contacto Test"):
    url = f"{URL_BASE}/v1/contactos"
    payload = {
        "nombre": nombre,
        "telefono": "775678890",
        "email": "contacto.test@mail.com"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    return response.json()["item"]["id_contacto"]


# TODO: 11. PUT 202 /v1/contacto?id_contacto=n actualiza contacto
def test_put_contacto_actualiza_exitosamente():
    id_contacto = _crear_contacto_para_pruebas("Contacto Update")
    url = f"{URL_BASE}/v1/contacto?id_contacto={id_contacto}"
    payload = {
        "nombre": "Contacto Actualizado",
        "telefono": "1234567890",
        "email": "actualizado@mail.com"
    }
    response = requests.put(url, json=payload)
    body = response.json()
    assert response.status_code == 202
    assert body["table"] == "contactos"
    assert body["count"] == 1
    assert body["message"] == "Contacto actualizado exitosamente"
    assert body["item"]["id_contacto"] == id_contacto
    assert body["item"]["email"] == "actualizado@mail.com"


# TODO: 12. PUT 400 /v1/contacto?id_contacto=n email sin arroba
def test_put_contacto_email_sin_arroba():
    id_contacto = _crear_contacto_para_pruebas("Contacto Email")
    url = f"{URL_BASE}/v1/contacto?id_contacto={id_contacto}"
    payload = {
        "nombre": "Contacto Error Email",
        "telefono": "1234567890",
        "email": "correoinvalido"
    }
    response = requests.put(url, json=payload)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "El email debe contener @"


# TODO: 13. PUT 400 /v1/contacto?id_contacto=x id como string
def test_put_contacto_id_string():
    url = f"{URL_BASE}/v1/contacto?id_contacto=x"
    payload = {
        "nombre": "Contacto Error Id",
        "telefono": "1234567890",
        "email": "ok@mail.com"
    }
    response = requests.put(url, json=payload)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "id no puede ser un string"


# TODO: 14. PUT 404 /v1/contacto?id_contacto=n no existe
def test_put_contacto_no_existe():
    url = f"{URL_BASE}/v1/contacto?id_contacto=99999999"
    payload = {
        "nombre": "Contacto Fantasma",
        "telefono": "1234567890",
        "email": "fantasma@mail.com"
    }
    response = requests.put(url, json=payload)
    body = response.json()
    assert response.status_code == 404
    assert body["table"] == "contactos"
    assert body["message"] == "este contacto no existe"


# TODO: 15. DELETE 202 /v1/contacto?id_contacto=n elimina contacto
def test_delete_contacto_exitosamente():
    id_contacto = _crear_contacto_para_pruebas("Contacto Delete")
    url = f"{URL_BASE}/v1/contacto?id_contacto={id_contacto}"
    response = requests.delete(url)
    body = response.json()
    assert response.status_code == 202
    assert body["table"] == "contactos"
    assert body["count"] == 1
    assert body["message"] == "Contacto eliminado exitosamente"
    assert body["item"]["id_contacto"] == id_contacto


# TODO: 16. DELETE 400 /v1/contacto?id_contacto= vacio
def test_delete_contacto_id_vacio():
    url = f"{URL_BASE}/v1/contacto?id_contacto="
    response = requests.delete(url)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "el campo no puede estar vacio"


# TODO: 17. DELETE 400 /v1/contacto?id_contacto=x id como string
def test_delete_contacto_id_string():
    url = f"{URL_BASE}/v1/contacto?id_contacto=x"
    response = requests.delete(url)
    body = response.json()
    assert response.status_code == 400
    assert body["table"] == "contactos"
    assert body["message"] == "id no puede ser un string"


# TODO: 18. DELETE 404 /v1/contacto?id_contacto=n no existe
def test_delete_contacto_no_existe():
    url = f"{URL_BASE}/v1/contacto?id_contacto=99999999"
    response = requests.delete(url)
    body = response.json()
    assert response.status_code == 404
    assert body["table"] == "contactos"
    assert body["message"] == "este contacto no existe"
