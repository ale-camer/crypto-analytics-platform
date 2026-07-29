# Issue #0: Initial Setup & Base Scaffolding

**Type**: `chore`  
**Branch**: `feature/day-0-setup`  
**Start Date**: 2026-07-25  
**Rule**: Day 0 = Scaffolding ONLY. No business code.

---

## Checklist

### 🌿 Git & Branches
- [x] `git init` in the project directory
- [x] Initial empty commit on `main`: `"chore: initial empty commit"`
- [x] `git checkout -b feature/day-0-setup`
- [ ] Create repository on GitHub (public: `crypto-analytics-platform`)
- [ ] `git remote add origin <url>` + `git push -u origin feature/day-0-setup`

**Verification**:
```bash
git branch          # → * feature/day-0-setup
git log --oneline   # → initial commit visible
```

---

### 🐍 Virtual Environment
- [x] `python3 -m venv .venv`
- [ ] `source .venv/bin/activate`
- [ ] `pip install -e ".[dev]"` (pytest, ruff, python-dotenv)
- [ ] Verify activation: `python --version`

**Verification**:
```bash
which python   # → should point to .venv/bin/python
```

---

### 📄 Configuration Files
- [x] `.gitignore` (excludes: `.venv/`, `.env`, `__pycache__/`, `.terraform/`)
- [x] `.env.example` (variables template, no real values)
- [x] `pyproject.toml` (metadata + empty deps + tools config)

**Verification**:
```bash
git status   # → .venv/ MUST NOT appear as untracked
cat .gitignore | grep .venv
```

---

### 📁 Directory Structure (empty with .gitkeep only)
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

### 📚 Documentation
- [x] `README.md` — draft with proposed architecture and issues roadmap
- [ ] `docs/architecture.md` — layers diagram and description (draft)
- [x] `docs/issue_0_setup.md` — this file

---

### ✅ Final Verification
- [ ] `git status` — only scaffolding files, no business code
- [ ] `.venv/` DOES NOT appear in `git status`
- [ ] All directories under `src/` are empty (only `.gitkeep`)
- [ ] `find src/ -name "*.py"` → no results

---

### 🚀 Issue #0 Closure Commit
- [ ] `git add .`
- [ ] `git commit -m "chore: project scaffolding"`
- [ ] `git push origin feature/day-0-setup`
- [ ] Create PR on GitHub: `feature/day-0-setup` → `main`

---

## Defined Following Issues

| Issue | Title | Content |
|-------|-------|---------|
| #1 | CoinGecko Extractor + Pydantic models | `src/extractors/`, `src/models/` |
| #2 | Polars Transformations | `src/transformers/` |
| #3 | BigQuery Loader + Terraform | `src/loaders/bigquery_loader.py`, `infra/` |
| #4 | Complete Airflow DAG | `dags/crypto_daily_pipeline.py` |
| #5 | Resilient GCS Archive | `src/loaders/gcs_loader.py` |

---

*P-02 Crypto Analytics Platform — Alejandro Camerlengo*
