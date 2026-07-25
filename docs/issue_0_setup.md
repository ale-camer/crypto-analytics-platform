# Issue #0: Setup Inicial & Scaffolding Base

**Tipo**: `chore`  
**Rama**: `feature/day-0-setup`  
**Fecha de inicio**: 2026-07-25  
**Regla**: Día 0 = SOLO scaffolding. Sin código de negocio.

---

## Checklist

### 🌿 Git & Ramas
- [x] `git init` en el directorio del proyecto
- [x] Commit inicial vacío en `main`: `"chore: initial empty commit"`
- [x] `git checkout -b feature/day-0-setup`
- [ ] Crear repo en GitHub (público: `crypto-analytics-platform`)
- [ ] `git remote add origin <url>` + `git push -u origin feature/day-0-setup`

**Verificación**:
```bash
git branch          # → * feature/day-0-setup
git log --oneline   # → commit inicial visible
```

---

### 🐍 Entorno Virtual
- [x] `python3 -m venv .venv`
- [ ] `source .venv/bin/activate`
- [ ] `pip install -e ".[dev]"` (pytest, ruff, python-dotenv)
- [ ] Verificar activación: `python --version`

**Verificación**:
```bash
which python   # → debe apuntar a .venv/bin/python
```

---

### 📄 Archivos de Configuración
- [x] `.gitignore` (excluye: `.venv/`, `.env`, `__pycache__/`, `.terraform/`)
- [x] `.env.example` (template de variables, sin valores reales)
- [x] `pyproject.toml` (metadata + deps vacías + config de herramientas)

**Verificación**:
```bash
git status   # → .venv/ NO debe aparecer como untracked
cat .gitignore | grep .venv
```

---

### 📁 Estructura de Directorios (solo vacíos con .gitkeep)
- [x] `src/extractors/.gitkeep`
- [x] `src/transformers/.gitkeep`
- [x] `src/loaders/.gitkeep`
- [x] `src/models/.gitkeep`
- [x] `src/utils/.gitkeep`
- [x] `dags/.gitkeep`
- [x] `tests/unit/.gitkeep`
- [x] `tests/integration/.gitkeep`
- [x] `infra/.gitkeep`
- [x] `docs/.gitkeep`

---

### 📚 Documentación
- [x] `README.md` — borrador con arquitectura propuesta y roadmap de issues
- [ ] `docs/architecture.md` — diagrama y descripción de capas (borrador)
- [x] `docs/issue_0_setup.md` — este archivo

---

### ✅ Verificación Final
- [ ] `git status` — solo archivos de scaffolding, sin código de negocio
- [ ] `.venv/` NO aparece en `git status`
- [ ] Todos los directorios bajo `src/` están vacíos (solo `.gitkeep`)
- [ ] `find src/ -name "*.py"` → ningún resultado

---

### 🚀 Commit de Cierre del Issue #0
- [ ] `git add .`
- [ ] `git commit -m "chore: project scaffolding"`
- [ ] `git push origin feature/day-0-setup`
- [ ] Crear PR en GitHub: `feature/day-0-setup` → `main`

---

## Issues Siguientes Definidos

| Issue | Título | Contenido |
|-------|--------|-----------|
| #1 | Extractor CoinGecko + modelos Pydantic | `src/extractors/`, `src/models/` |
| #2 | Transformaciones Polars | `src/transformers/` |
| #3 | BigQuery Loader + Terraform | `src/loaders/bigquery_loader.py`, `infra/` |
| #4 | DAG Airflow completo | `dags/crypto_daily_pipeline.py` |
| #5 | GCS Archive resiliente | `src/loaders/gcs_loader.py` |

---

*P-02 Crypto Analytics Platform — Alejandro Camerlengo*
