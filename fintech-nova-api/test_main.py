from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestEndpointsBasicos:
    def test_status_operacional(self):
        resp = client.get("/status")
        assert resp.status_code == 200
        assert resp.json()["Estado"] == "Operacional"

    def test_health_responde(self):
        # /health puede devolver 200 (sano) o 503 (no sano según psutil),
        # pero siempre debe responder, nunca caerse.
        resp = client.get("/health")
        assert resp.status_code in (200, 503)


class TestEvaluacionRiesgo:
    def test_menor_de_edad_rechazado(self):
        resp = client.post(
            "/evaluar-riesgo",
            json={"edad": 17, "ingresos": 5000, "deudas": 100},
        )
        assert resp.status_code == 200
        assert resp.json()["resultado"] == "Rechazado (Menor de edad)"

    def test_score_alto_aprobado(self):
        resp = client.post(
            "/evaluar-riesgo",
            json={"edad": 30, "ingresos": 5000, "deudas": 1000},
        )
        assert resp.status_code == 200
        assert resp.json()["resultado"] == "Aprobado"

    def test_score_bajo_en_revision(self):
        resp = client.post(
            "/evaluar-riesgo",
            json={"edad": 30, "ingresos": 1500, "deudas": 1000},
        )
        assert resp.status_code == 200
        assert resp.json()["resultado"] == "En Revision"

    def test_payload_invalido_retorna_422(self):
        resp = client.post(
            "/evaluar-riesgo",
            json={"edad": "treinta", "ingresos": 1500, "deudas": 1000},
        )
        assert resp.status_code == 422


class TestDatosFinancieros:
    def test_sin_token_retorna_401(self):
        resp = client.get("/datos-financieros/123")
        assert resp.status_code == 401

    def test_con_token_valido_retorna_200(self):
        resp = client.get(
            "/datos-financieros/123",
            headers={"x-api-key": "fintech2026"},
        )
        assert resp.status_code == 200
        assert resp.json()["cliente_id"] == 123
        assert resp.json()["historial"] == "Limpio"