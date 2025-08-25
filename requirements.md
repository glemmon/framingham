# requirements.md

## Product Overview
- Purpose: Provide a browser‑based interface for exploring cardiology survival curves from the Framingham dataset.
- Target Users: Research scientists.
- Core Objectives:
  1) For each outcome, show the effect of each predictor on the hazard rate using Cox proportional hazards.
  2) For each outcome, show the unadjusted Kaplan–Meier (KM) survival curve.
- Framework & Constraints: Python + Flask; single‑page site; HTTP (not HTTPS); single CPU; PyTest for tests.

## Library Guidance
- Use Pandas, NumPy, SciPy, and statsmodels for data/statistics.
- Use lifelines and/or scikit‑survival (sksurv) for survival analysis (KM, Cox PH).
- Use Matplotlib and Seaborn for plots and visualizations.
- Other free PyPI packages may be used (e.g., cachetools, pydantic).

## User Stories
1. Preload Framingham.csv to analyze without uploads.
2. Choose an outcome and see an unadjusted KM curve (with 95% CI).
3. Select predictors and run a Cox PH model (HR, CI, p‑value).
4. Provide default time/event mappings per outcome with override capability.
5. Present clear plots and tables (labels, legends, captions) and support PNG/SVG export.
6. Offer filters (exclude prevalent disease; restrict to PERIOD=3 for HDLC/LDLC) and data quality flags (smoking inconsistencies).
7. Surface graceful, actionable errors (convergence, collinearity, invalid selections).
8. Maintain a single‑page responsive UI.

## Acceptance Criteria (EARS)
### Data & Initialization
- When the app starts then the server shall load Framingham.csv and expose column metadata.
- When the dataset is missing/unreadable then the UI shall show a blocking error and disable analysis.

### Outcome Mapping & Selection
- When the user picks a predefined outcome then the system shall auto‑map the corresponding event/time columns (with option to override) and document the mapping in results.

### Kaplan–Meier (KM)
- When valid time/event columns are set then the system shall compute KM with lifelines/sksurv and plot survival with 95% CI, labeled axes, legend, title.
- When zero events then the curve shall be flat at 1.0 with notice.
- When all events at t=0 then the curve shall be flat at 0.0 with notice.

### Cox Proportional Hazards
- When time/event and ≥1 predictors are selected then the system shall fit Cox PH via lifelines/sksurv and display HR, 95% CI, and p‑value.
- When categorical predictors are included then one‑hot encode (drop one baseline) and report baseline.
- When collinearity or quasi‑separation is detected then list implicated predictors and halt with guidance.
- When model non‑converges then show a non‑blocking error with suggestions.
- When basic PH checks are requested then provide simple notices; full diagnostics out of scope v1.

### Filters, Missingness, Data Quality
- When modeling incident outcomes then the user can exclude prevalent disease rows.
- When HDLC/LDLC are used without PERIOD=3 then warn and offer to filter to PERIOD=3.
- When smoking inconsistencies are present then report counts and offer leave/coerce/drop.
- When predictors have missing values then allow drop or impute and note method in output.

### Plot Export & Reporting
- When Download Plot is clicked then the current KM or Cox plot downloads as PNG or SVG.
- When Results Summary opens then list filters, mapping, encoding, tie method, and missingness handling.

### UI & Responsiveness
- When the page loads then the entire experience is a single‑page interface over HTTP.
- When long computations run then the UI shows a busy indicator and remains responsive.
