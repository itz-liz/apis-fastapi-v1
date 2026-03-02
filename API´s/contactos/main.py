from datetime import datetime
from fastapi import FastAPI
from fastapi import Query
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3 as sqlite
from typing import Optional

app = FastAPI()

DB_PATH = "agenda.db"


class ContactoCreate(BaseModel):
    nombre: str
    telefono: str
    email: str


def _utc_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _get_db_connection() -> sqlite.Connection:
    db = sqlite.connect(DB_PATH)
    db.row_factory = sqlite.Row
    return db


def _init_db() -> None:
    db = _get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contactos (
                id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
            """
        )
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    _init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Error de validacion"
    status_code = 400
    for error in exc.errors():
        loc = error.get("loc", [])
        if error.get("type") == "value_error.missing":
            message = "Campos vacios"
            status_code = 401
        error_type = error.get("type") or ""
        if any(param in loc for param in ("limit", "skip", "id_contacto")) and (
            error_type == "value_error.number.not_ge"
            or "greater_than_equal" in error_type
        ):
            message = "valores negativos"

    return JSONResponse(
        status_code=status_code,
        content={
            "table": "contactos",
            "item": {},
            "count": 0,
            "datetime": _utc_timestamp(),
            "message": message
        }
    )

@app.get("/",
 status_code=202,
 summary="Endpoint raíz",
 description= "Bienvenido a la API de agenda")
def get_root():
    response = {
        "message": "API de la agenda",
        "datatime": _utc_timestamp()
        }
    return response

@app.get(
    "/v1/contactos",
    status_code=202,
    summary="Endpoint que ingresa los contactos paginados",
    description= """Endpoint que ingresa los contactos paginados,
    utiliza los siguientes query params:
    limit:int -> Indica el número de registros a regresar
    skip:int -> Indica el número de registros a omitir"""
)
async def get_contactos(
    limit: Optional[str] = Query(None),
    skip: Optional[str] = Query(None)
):
    normalized_limit = limit.strip().lower() if isinstance(limit, str) else None
    normalized_skip = skip.strip().lower() if isinstance(skip, str) else None

    if normalized_limit in (None, "", "null", "none") and normalized_skip in (None, "", "null", "none"):
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit y skip no pueden ser nulos"
            }
        )

    if normalized_limit in (None, "", "null", "none"):
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit no puede ser nulo"
            }
        )

    if normalized_skip in (None, "", "null", "none"):
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "skip no puede ser nulo"
            }
        )

    limit_is_text = False
    skip_is_text = False

    try:
        limit_value = int(limit)
    except ValueError:
        limit_is_text = True

    try:
        skip_value = int(skip)
    except ValueError:
        skip_is_text = True

    if limit_is_text and skip_is_text:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit y skip no pueden ser un conjunto de letras"
            }
        )

    if limit_is_text:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit no puede ser un string"
            }
        )

    if skip_is_text:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "skip no puede ser un string"
            }
        )

    if limit_value < 0 and skip_value < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit y skip no pueden ser negativos"
            }
        )
        
    if limit_value < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit no puede ser negativo"
            }
        )
    if skip_value < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "skip no puede ser negativo"
            }
        )

    if limit_value == 0:
        return JSONResponse(
            status_code=407,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "limit no puede ser cero"
            }
        )
    
    if skip_value == 0:
        return JSONResponse(
            status_code=407,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "skip no puede ser cero"
            }
        )   

    # TODo: Quiero una hagas un error en este comentario donde se evalue si
    
    try:
        db = _get_db_connection()
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM contactos LIMIT ? OFFSET ?", (limit_value, skip_value))
            contactos = cursor.fetchall()
            items = [dict(row) for row in contactos]

            
        finally:
            db.close()

        data = {
            "table": "contactos",
            "items": items,
            "count": len(items),
            "datetime": _utc_timestamp(),
            "message": "Datos consultados exitosamente",
            "limit": limit_value,
            "skip": skip_value
        }
        return JSONResponse(
            status_code=202,
            content=data
        )
    except Exception as e:
        print(f"Error al consultar la base de datos: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "Error al consultar la base de datos",
                "limit": limit_value,
                "skip": skip_value
                }
            )


@app.post(
    "/v1/contactos",
    status_code=201,
    summary="Endpoint para insertar un contacto",
    description="""Endpoint para insertar un contacto.
    Valida campos obligatorios."""
)
async def create_contacto(contacto: ContactoCreate):
    if not contacto.nombre.strip() or not contacto.telefono.strip() or not contacto.email.strip():
        return JSONResponse(
            status_code=401,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "Campos vacios"
            }
        )

    try:
        db = _get_db_connection()
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO contactos (nombre, email, telefono) VALUES (?, ?, ?)",
                (contacto.nombre.strip(), contacto.email.strip(), contacto.telefono.strip())
            )
            db.commit()
            new_id = cursor.lastrowid
        finally:
            db.close()

        data = {
            "table": "contactos",
            "item": {
                "id_contacto": new_id,
                "nombre": contacto.nombre.strip(),
                "email": contacto.email.strip(),
                "telefono": contacto.telefono.strip()
            },
            "datetime": _utc_timestamp(),
            "message": "Contacto insertado exitosamente"
        }
        return JSONResponse(status_code=201, content=data)
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Error en la base de datos",
                "datetime": _utc_timestamp()
            }
        )


@app.get(
    "/v1/contactos/{id_contacto}",
    status_code=202,
    summary="Endpoint para buscar un contacto",
    description="Endpoint para buscar un contacto por id_contacto."
)
async def get_contacto(id_contacto: int):
    if id_contacto < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": _utc_timestamp(),
                "message": "El id no puede ser negativo"
            }
        )
    try:
        db = _get_db_connection()
        try:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM contactos WHERE id_contacto = ?",
                (id_contacto,)
            )
            contacto = cursor.fetchone()
        finally:
            db.close()

        if contacto is None:
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "item": {},
                    "count": 0,
                    "datetime": _utc_timestamp(),
                    "message": "Contacto no encontrado"
                }
            )

        data = {
            "table": "contactos",
            "items": [dict(contacto)],
            "count": 1,
            "datetime": _utc_timestamp(),
            "message": "Datos consultados exitosamente"
        }
        return JSONResponse(status_code=202, content=data)
    except Exception as e:
        print(f"Error al buscar en la base de datos: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Error al buscar el registro",
                "datetime": _utc_timestamp()
            }
        )