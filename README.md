# 🛡️ DevSecOps Demo - CI/CD con Gestión de Vulnerabilidades

API de demostración que integra herramientas de seguridad en un pipeline CI/CD.

## 🚀 Inicio Rápido

### Ejecutar localmente

```bash
# Instalar dependencias
pip install uv
uv pip install --system -r pyproject.toml

# Ejecutar
python main.py
```

Acceder a Swagger: <http://localhost:8000/docs>

### Ejecutar con Docker

```bash
docker build -t devsecops-demo .
docker run -p 8000:8000 devsecops-demo
```

---

## 📋 Pipelines CI/CD

Los pipelines se activan en `push` y `pull_request` a `main`. Están separados en workflows independientes:

### Workflows Disponibles

| Archivo | Nombre | Descripción |
|---------|--------|-------------|
| `sast.yml` | 🔍 SAST | Bandit + CodeQL para análisis estático |
| `dependency-scan.yml` | 📦 Dependency Scan | pip-audit, Safety, OWASP DC |
| `tests.yml` | 🧪 Tests | pytest con cobertura |
| `build-scan.yml` | 🐳 Build & Container Scan | Docker build + Trivy |
| `security-gate.yml` | 🚦 Security Gate | Resumen de seguridad |
| `deploy.yml` | 🚀 Deploy | Deploy a producción (solo main) |

### Flujo de Ejecución

```
┌─────────────┐   ┌──────────────────┐   ┌─────────┐
│  sast.yml   │   │dependency-scan.yml│   │tests.yml│
│  (Bandit +  │   │   (pip-audit,    │   │(pytest) │
│   CodeQL)   │   │  Safety, OWASP)  │   │         │
└──────┬──────┘   └────────┬─────────┘   └────┬────┘
       │                   │                  │
       │                   ▼                  │
       │          ┌────────────────┐          │
       └─────────►│ build-scan.yml │◄─────────┘
                  │  (Docker +     │
                  │   Trivy)       │
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │security-gate.yml│
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │  deploy.yml    │
                  │  (solo main)   │
                  └────────────────┘
```

---

## 🔐 Herramientas de Seguridad Integradas

| Herramienta | Tipo | Qué detecta |
|-------------|------|-------------|
| **CodeQL** | SAST | Vulnerabilidades en código (SQL Injection, XSS, etc.) |
| **Bandit** | SAST | Problemas de seguridad en Python |
| **pip-audit** | SCA | CVEs en dependencias Python |
| **Safety** | SCA | Vulnerabilidades conocidas en paquetes |
| **OWASP Dependency-Check** | SCA | CVEs en dependencias |
| **Trivy** | Container | Vulnerabilidades en imagen Docker |

---

## ⚠️ Reglas de Fallo del Pipeline

| Severidad | Acción |
|-----------|--------|
| **CRITICAL** | ❌ Pipeline **FALLA** |
| **HIGH** | ⚠️ Warning (revisar) |
| **MEDIUM/LOW** | ℹ️ Solo reporte |

---

## 🎯 Vulnerabilidades Intencionales (Demo)

### Código Vulnerable (detectado por SAST)

- `GET /users/search/vulnerable` → **SQL Injection** (Bandit B608)
- `POST /products/import/vulnerable` → **Deserialización insegura** (Bandit B301)

### Fuentes de Vulnerabilidades en Pipeline

| Herramienta | Qué detecta |
|-------------|-------------|
| **Bandit** | SQL Injection, pickle, hardcoded passwords |
| **CodeQL** | Vulnerabilidades semánticas en código |
| **pip-audit** | CVEs en dependencias transitivas |
| **Safety** | Vulnerabilidades conocidas en paquetes |
| **Trivy** | Vulnerabilidades en imagen Docker (OS + libs) |

### Código Vulnerable

- `GET /users/search/vulnerable` → SQL Injection
- `POST /products/import/vulnerable` → Deserialización insegura

---

## 📁 Estructura del Proyecto

```
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicación FastAPI
│   ├── config.py        # Configuración
│   ├── models/          # Modelos Pydantic
│   │   ├── user.py
│   │   └── product.py
│   └── routers/         # Endpoints
│       ├── health.py
│       ├── users.py
│       └── products.py
├── tests/               # Tests unitarios
├── .github/workflows/
│   └── ci.yml           # Pipeline CI/CD
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 📊 Ver Reportes

Los reportes se generan como artifacts en GitHub Actions:

- `bandit-report` - Análisis SAST
- `pip-audit-report` - Vulnerabilidades en dependencias
- `safety-report` - CVEs conocidas
- `trivy-reports` - Escaneo de contenedor
- `owasp-dependency-check-report` - OWASP DC

---

## 🧪 Ejecutar Tests Localmente

```bash
pip install pytest pytest-cov httpx
pytest tests/ -v --cov=app
```

---

## 📝 Licencia

Proyecto de demostración académica para DevSecOps.
