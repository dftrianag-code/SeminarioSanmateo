# Informe de Auditoría y Hardening de Seguridad

## Proyecto Integrador
### Arquitectura, Seguridad y Automatización de una API de Predicción en la Nube

### Integrantes

- David Felipe Triana González
- Frank Leonardo Carvajal Rojas
- Juan Felipe Escobar Flórez

---

# 1. Objetivo

Realizar una auditoría básica de seguridad sobre la API desarrollada en FastAPI con el propósito de identificar vulnerabilidades y aplicar mecanismos de hardening para proteger la información expuesta por el sistema.

---

# 2. Escaneo Inicial

Se realizó un análisis utilizando la herramienta Nmap para identificar los puertos y servicios expuestos por la aplicación.

Comando ejecutado:

```bash
nmap localhost
```

Resultados obtenidos:

- Puerto 8000 abierto.
- Servicio HTTP activo.
- Aplicación disponible para ser consumida mediante peticiones HTTP.

### Evidencia

Imagen:

`practica_sql/evidencias/1_nmap.png`

---

# 3. Vulnerabilidad Identificada

Durante el análisis se encontró que el endpoint:

```text
/secure/users/{username}
```

procesa información relacionada con los usuarios y, si no se implementan controles de acceso, podría ser utilizado por usuarios no autorizados.

Adicionalmente, la aplicación cuenta con un endpoint vulnerable:

```text
/vulnerable/users/{username}
```

el cual utiliza concatenación directa en las consultas SQL, permitiendo ataques de SQL Injection.

### Riesgos asociados

- Exposición de información sensible.
- Alteración del comportamiento esperado de la consulta.
- Acceso no autorizado a los datos.
- Pérdida de confidencialidad.

### Evidencia

Imagen:

`evidencias/2_endpoint_vulnerable.png`

---


# 4. Implementación del Hardening

Con el fin de proteger la aplicación se implementaron las siguientes medidas:

- Uso de consultas parametrizadas en el endpoint seguro.
- Incorporación de cabeceras HTTP de seguridad.
- Implementación de autenticación mediante API Key.
- Restricción de acceso a los recursos protegidos.

Se configuró el encabezado:

```text
x-api-key
```

con el valor:

```text
fintech2026
```

de manera que únicamente los usuarios autorizados puedan acceder al endpoint protegido.

---

# 5. Validación del Mecanismo de Seguridad

Se realizaron pruebas accediendo al endpoint:

```text
/secure/users/{username}
```

sin proporcionar credenciales válidas.

La API respondió con el código:

```text
401 Unauthorized
```

confirmando que el mecanismo de autenticación funciona correctamente y que las solicitudes no autorizadas son rechazadas.

### Evidencia

Imagen:

`evidencias/3_401_unauthorized.png`

---

# 6. Acceso Autorizado

Posteriormente se realizaron pruebas enviando correctamente el encabezado:

```text
x-api-key: fintech2026
```

La aplicación permitió el acceso al recurso solicitado y devolvió la información correspondiente del usuario consultado.

### Evidencia

Imagen:

`evidencias/4_acceso_autorizado.png`

---

# 7. Conclusiones

- El análisis permitió identificar vulnerabilidades relacionadas con la exposición de información y ataques de SQL Injection.
- El escaneo con Nmap permitió verificar los servicios disponibles en la aplicación.
- Se implementaron medidas de hardening para fortalecer la seguridad.
- Se añadió autenticación mediante API Key para restringir el acceso al endpoint protegido.
- Las peticiones sin credenciales válidas son rechazadas con el código HTTP 401 Unauthorized.
- Las medidas implementadas mejoraron significativamente la protección de la API.

---
