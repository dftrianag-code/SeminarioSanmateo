# Seminario-ARQUITECTURAS-DIGITALES-SEGURAS-Y-AUTOMATIZADAS

## PROYECTO: Proyecto Final Integrador: Arquitectura, Seguridad y  Automatización de una API de Predicción en la Nube
### Roslaysoft x FinTech Nova 

## DESCRIPCIÓN DEL PROYECTO: 
En la actualidad, las aplicaciones no operan de forma aislada; viven en ecosistemas 
dinámicos en la nube que requieren ser rápidos, seguros y escalables. Durante este 
seminario, los estudiantes actuarán como Arquitectos Cloud para una empresa simulada 
de tecnología.

## El Caso de Estudio: "FinTech Nova" y la API de Riesgo Crediticio
El Contexto (El Roleplay para los estudiantes): La firma consultora Roslaysoft ha cerrado 
un contrato con FinTech Nova, una startup financiera de rápido crecimiento que ofrece 
microcréditos 100% digitales. Actualmente, FinTech Nova tiene su motor de "Evaluación de 
Riesgo Crediticio" (Credit Scoring) corriendo en un servidor local antiguo que se satura los 
fines de semana.
Han contratado a los estudiantes para que tomen el código base de ese motor (la API en 
FastAPI) y diseñen una arquitectura en la nube que sea segura, escalable y automatizada.


## Integrantes del Grupo 

| GRUPO 9 |  

| DAVID FELIPE TRIANA GONZÁLEZ | [@usuario1](https://github.com/dftrianag-code/DavidTriana.git) | 

| FRANK LEONARDO CARVAJAL ROJAS | [@usuario2](https://github.com/flcarvajalr-collab/frank) | 

| JUAN FELIPE ESCOBAR FLOREZ |  | 


# Laboratorio 1 — Arquitectura As-Is 

 

### URL del Codespace 

### URL pública de APPI SeminarioSanMateo Bifurcado de RoslayBautista/SeminarioSanmateo:

https://laughing-yodel-p7jp54gxj9gr37qjr-8000.app.github.dev/ 


https://laughing-yodel-p7jp54gxj9gr37qjr-8000.app.github.dev/docs 

### URL pública de APPI Seminario-ARQUITECTURAS-DIGITALES-SEGURAS-Y-AUTOMATIZADAS de mi repositorio:

https://fuzzy-doodle-p75697xv447fr4v6-8000.app.github.dev/


 
### Diagrama Arquitectonico As-Is 

El siguiente diagrama representa el estado actual del sistema de evaluación de riesgo crediticio de FinTech Nova desplegado en GitHub Codespaces: 

![Diagrama As - Is](docs/Diagramas/Diagrama%20As-Is.drawio.png)

 
### Version interactiva (Mermaid) 

```mermaid 

graph TD 

    %% ======================================================== 

    %% TITULO DEL DIAGRAMA 

    %% Arquitectura As-Is — API Riesgo Crediticio — FinTech Nova 

    %% Laboratorio 1 — Roslaysoft Consulting 

    %% ======================================================== 

 

    %% ── ACTOR EXTERNO ───────────────────────────────────── 

       Cliente["👤 Cliente FinTech Nova<br>App Movil / Web Browser"]

    subgraph Internet["🌐 INTERNET / Red Publica"]
        Canal["HTTPS / TLS 1.3<br>Puerto publico del Codespace"]
    end

    subgraph Codespaces["☁️ GitHub Codespaces | Microsoft Azure URL: https://fuzzy-doodle-p75697xv447fr4v6-8000.app.github.dev"]

        subgraph Contenedor["📦 Contenedor Linux Efimero | VS Code Server"]

            subgraph FastAPI["⚙️ FastAPI Application | uvicorn | Puerto 8000"]

                EP1["POST /evaluar-riesgo<br>Scoring Crediticio"]

                EP2["GET /status<br>Health Check"]

                EP3["GET /datos-financieros/{id}<br>⚠️ VULNERABLE - Sin Autenticacion"]

            end

        end

    end

    Cliente -->|"HTTPS Request<br>JSON Payload"| Canal

    Canal -->|"HTTP interno<br>Puerto 8000"| FastAPI

    FastAPI -->|"Procesa request"| EP1

    FastAPI -->|"Procesa request"| EP2

    FastAPI -->|"Procesa request"| EP3

    EP1 -.->|"JSON Response<br>Aprobado / Rechazado / En Revision"| Cliente

    EP2 -.->|"JSON Response<br>Status: healthy"| Cliente

    EP3 -.->|"JSON Response<br>Historial sin restriccion"| Cliente

    classDef actor fill:#EBF5FB,stroke:#1A5C9A,stroke-width:2px,color:#0D2B55

    classDef endpoint_safe fill:#C8DDEF,stroke:#1A5C9A,stroke-width:2px,color:#0D2B55

    classDef endpoint_monitor fill:#D5F5E3,stroke:#1E8449,stroke-width:2px,color:#1E8449

    classDef endpoint_vuln fill:#FADBD8,stroke:#C0392B,stroke-width:3px,color:#C0392B

    class Cliente actor

    class EP1 endpoint_safe

    class EP2 endpoint_monitor

    class EP3 endpoint_vuln


``` 

