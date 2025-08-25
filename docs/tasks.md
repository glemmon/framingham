# tasks.md

## 0) Conventions
- Format: Each task has description, expected outcome, dependencies, resources.
- Libraries: Pandas, NumPy, SciPy, statsmodels, lifelines, sksurv (optional), Matplotlib, Seaborn, PyPI utilities.
- Framework: Python 3 + Flask; PyTest for tests.

## 1) Project Setup
### 1.1 Repo & Skeleton
- Description: Create project tree (app/, core/, ui/, tests/, logging/), add requirements.txt
- Outcome: Structured repo committed
- Deps: —
- Resources: design.md, requirements.md

### 1.2 Dependencies
- Description: Install requirements.txt
- Outcome: Dev env ready
- Deps: 1.1

### 1.3 Lint/Test
- Description: Configure pytest; optional mypy/flake8
- Outcome: `pytest` runs
- Deps: 1.1, 1.2

## 2) Data Layer
### 2.1 Loader
- Description: Load Framingham.csv; cache DataFrame
- Outcome: Data available in memory
- Deps: 1.2

### 2.2 Typing & Validation
- Description: Infer numeric/binary/categorical; validate event/time
- Outcome: /api/columns returns correct types
- Deps: 2.1

### 2.3 Outcome Mapping
- Description: default outcome→(event,time); reverse lookup
- Outcome: UI drop‑down works; mapping in results
- Deps: 2.1

## 3) Filters & Preprocessing
### 3.1 Prevalent Exclusions
- Description: Exclude PREV* rows for incident outcomes
- Outcome: Counts reflect exclusion
- Deps: 2.*

### 3.2 PERIOD Filter
- Description: Filter to PERIOD=3 for lipids
- Outcome: Usable N reported; warnings when not filtered
- Deps: 2.*

### 3.3 Smoking Consistency
- Description: Detect CURSMOKE=0 with CIGPDAY>0; leave/coerce/drop
- Outcome: Option applied; summary notes
- Deps: 2.*

### 3.4 Missingness
- Description: Drop vs impute (mean/mode) for predictors
- Outcome: Chosen method annotated
- Deps: 2.*

## 4) Analysis Engines
### 4.1 KM (lifelines)
- Description: KMF wrapper returning survival+CI JSON
- Outcome: /api/km returns curve and meta
- Deps: 2.*, 3.*

### 4.2 Cox (lifelines)
- Description: CPH wrapper with one‑hot encoding
- Outcome: HR/CI/p table, baselines, convergence flag
- Deps: 2.*, 3.*

### 4.3 Optional sksurv
- Description: Backend toggle for Cox
- Outcome: Verification path
- Deps: 4.2

## 5) Plotting
### 5.1 KM Plot
- Description: Step + CI band; PNG/SVG export
- Outcome: /api/export_plot (km) works
- Deps: 4.1

### 5.2 Cox Forest
- Description: HR with 95% CI bars; log scale
- Outcome: /api/export_plot (cox) works
- Deps: 4.2

## 6) Flask App & Routes
### 6.1 App Factory
- Description: create_app(); preload dataset
- Outcome: run.py starts server
- Deps: 2.*, 4.*

### 6.2 Routes
- Description: /, /api/columns, /api/km, /api/cox, /api/export_plot, /health
- Outcome: Endpoints stable and documented
- Deps: 6.1

### 6.3 Errors & Logging
- Description: Friendly JSON errors, structured logs
- Outcome: Actionable messages; logs capture failures
- Deps: 6.2

## 7) UI
### 7.1 SPA
- Description: index.html with controls & tabs
- Outcome: Single‑page UX
- Deps: 6.*

### 7.2 JS Client
- Description: Fetch to APIs; render plots/tables
- Outcome: End‑to‑end flow KM→Cox→Export
- Deps: 7.1

### 7.3 Downloads
- Description: Download PNG/SVG
- Outcome: Files saved locally
- Deps: 5.*

## 8) Testing
### 8.1 Unit
- Description: Validate loaders, mappings, filters, KM, Cox
- Outcome: ≥85% coverage on core logic
- Deps: 2–4

### 8.2 API
- Description: Contract tests for each endpoint
- Outcome: Correct JSON and images
- Deps: 6.*

### 8.3 Perf
- Description: KM ≤2s; Cox ≤5s
- Outcome: Benchmarks pass
- Deps: 4–5

### 8.4 Accessibility
- Description: Basic keyboard/ARIA checks
- Outcome: Pass basic checks
- Deps: 7.*

## 9) Deployment
### 9.1 Health
- Description: /health for ops
- Outcome: Monitoring-ready
- Deps: 6.2

### 9.2 Packaging
- Description: Dockerfile/Procfile (optional)
- Outcome: Reproducible builds
- Deps: 6.*
