# design.md (v1.1 — updated libraries)

## 0) What changed (vs v1.0)
- KM & Cox PH: Implemented with lifelines (primary).
- Optional backend: scikit-survival (sksurv) for verification and future models.
- Statsmodels: supplemental inference/stats if needed.
- Plots: Matplotlib backbone; Seaborn for improved aesthetics.
- PyPI utilities: allowed (e.g., cachetools, pydantic).

## 1) System Architecture
### 1.1 Overview
- Client (SPA): HTML + vanilla JS, fetch API calls. Renders plots/tables, supports downloads.
- Server (Flask):
  - Dataset registry: load Framingham.csv, provide metadata.
  - Validation/filters: enforce mappings, handle missingness, apply prevalent-disease and period filters, detect smoking inconsistencies.
  - KM Engine: lifelines.KaplanMeierFitter.
  - Cox Engine: lifelines.CoxPHFitter (Efron ties).
  - Diagnostics: basic PH checks; detailed diagnostics out of scope v1.
  - Plotting: Matplotlib + Seaborn.
  - Caching: in-memory (e.g., cachetools LRU).

### 1.2 Module layout
(app/, core/, ui/, logging/ as implemented in this codebase.)

## 2) Data Models & Schemas
- Column types inferred as numeric/binary/categorical; lipids (HDLC/LDLC) mainly for PERIOD=3.
- Default outcome → (event, time) mapping for Angina, MI, CHD, Stroke, CVD, Mortality, Hypertension.
- JSON contracts for /api/columns, /api/km, /api/cox, /api/export_plot, /health.

## 3) API Contracts (condensed)
- GET /api/columns → {columns, types, defaults}
- POST /api/km → {survival[], meta{}}
- POST /api/cox → {rows[], meta{}, warnings[]}
- POST /api/export_plot → PNG/SVG image
- GET /health → {"status":"ok","dataset_loaded":true}

## 4) Implementation Considerations
- One-hot encode categoricals with drop-first; track baseline levels.
- Cox: robust=True, tie_method="efron"; catch convergence/collinearity; provide warnings.
- Filters: prevalent exclusions; PERIOD filter; smoking inconsistency remediation.
- Plotting: KM step + CI; Cox forest/log-HR plot; labeled axes and legend.

## 5) Technical Assumptions
- Dataset bundled and loads at startup; single CPU; HTTP; SPA.
- Libraries present: Pandas, NumPy, SciPy, lifelines, statsmodels, Matplotlib, Seaborn; sksurv optional.
