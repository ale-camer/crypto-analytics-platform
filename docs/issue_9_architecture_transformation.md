# Issue #9: Architecture Documentation — Transformation Layer and Polars ADR

**Branch**: `docs/issue-9-arch-transformation` (based on `develop`)  
**Objective**: Document the architecture of the data transformation layer (`PriceTransformer`) and add the Architectural Decision Record (ADR) for using Polars in `docs/architecture.md`.

---

## Step 1 — Create the branch from `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b docs/issue-9-arch-transformation
```

---

## Step 2 — Update `docs/architecture.md`

File: `docs/architecture.md`

Add a new section for the Transformation Layer after the Extraction Layer, and a new ADR for Polars:

1. **Transformation Layer Overview (`src/transformers/price_transformer.py`)**:
   - Role of `PriceTransformer` in converting validated `PriceRecord` instances into structured analytical DataFrames.
   - Utilization of Polars for high-performance, memory-efficient data processing.
   - Implementation of Technical Indicators (RSI, MACD, Bollinger Bands) using native Polars expressions (e.g., `ewm_mean`, `rolling_mean`, `rolling_std`).
   - Graceful handling of missing historical data (yielding nulls) without crashing the pipeline.

2. **Architectural Decision Record (ADRs)**:
   - **ADR-003**: Selection of Polars over Pandas for Data Transformation.
     - **Status**: Approved.
     - **Context**: The pipeline requires high-speed calculations for technical indicators across multiple cryptocurrency time-series.
     - **Decision**: Adopt Polars due to its Rust-based engine, multi-threading capabilities, and strict schema enforcement.
     - **Consequences**: Significantly faster execution times and lower memory footprint compared to Pandas, but requires adopting the Polars Expression API syntax.

---

## Step 3 — Commit and Push

```bash
git add docs/architecture.md docs/issue_9_architecture_transformation.md
git commit -m "docs: architecture for transformation layer and Polars ADR"
git push origin docs/issue-9-arch-transformation
```

---

## Step 4 — Create PR, Merge and Close Issue

Create the PR to `develop`:
```bash
gh pr create \
  --title "docs: Issue #9 — Transformation layer architecture and Polars ADR" \
  --body "Documents the PriceTransformer layer and ADR-003." \
  --base develop \
  --head docs/issue-9-arch-transformation
```

Merge it:
```bash
gh pr merge <N> --squash --delete-branch
```

**Close the Issue manually**:
```bash
gh issue close 9 --comment "Completed and integrated in develop"
```

Update local environment:
```bash
git checkout develop
git pull origin develop
```
