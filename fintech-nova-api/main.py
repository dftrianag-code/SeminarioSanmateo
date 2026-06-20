from fastapi import FastAPI, HTTPException
from health_check import run_all_checks
from pydantic import BaseModel

app = FastAPI(  
 title="FinTech Nova - Motor de Riesgo",
 description="API de evaluacion de riesgo crediticio",
 version="1.0.0"
)

# Endpoint de verificación de salud
@app.get("/health")
def health_check_endpoint():

    result = run_all_checks()

    if result["status"] == "unhealthy":
        raise HTTPException(
            status_code=503,
            detail=result
        )

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
def obtener_historial(id_cliente: int):
 return {
 "cliente_id": id_cliente,
 "historial": "Limpio",
 "score_interno": 750
 }


