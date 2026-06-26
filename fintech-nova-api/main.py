from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from health_check import run_all_checks
from pydantic import BaseModel

app = FastAPI(
    title="FinTech Nova - Motor de Riesgo",
    description="API de evaluacion de riesgo crediticio",
    version="1.0.0"
)

# ==================================================
# AUTENTICACIÓN — Control de acceso (Laboratorio 2)
# ==================================================

API_KEY = "fintech2026"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def verificar_token(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de FinTech Nova. El sistema está en línea."}


@app.get("/health")
def health_check_endpoint():
    result = run_all_checks()
    if result["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=result)
    return result


class SolicitudCredito(BaseModel):
    edad: int
    ingresos: float
    deudas: float


@app.get("/status")
def get_status():
    return {"Estado": "Operacional", "servidor": "Nodo-01"}


@app.post("/evaluar-riesgo")
def evaluar_riesgo(solicitud: SolicitudCredito):
    score = solicitud.ingresos - solicitud.deudas
    if solicitud.edad < 18:
        resultado = "Rechazado (Menor de edad)"
    elif score > 1000:
        resultado = "Aprobado"
    else:
        resultado = "En Revision"
    return {"resultado": resultado, "score_simulado": score}


@app.get("/datos-financieros/{id_cliente}")
def obtener_historial(id_cliente: int, api_key: str = Depends(verificar_token)):
    return {
        "cliente_id": id_cliente,
        "historial": "Limpio",
        "score_interno": 750
    }
# Comentario agregado para demo en vivo Thu Jun 25 05:51:04 UTC 2026
# Comentario agregado para demo en vivo Thu Jun 25 13:28:56 UTC 2026
# Comentario agregado para demo en vivo Fri Jun 26 01:47:10 UTC 2026
