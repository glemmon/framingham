# test.md — Test Plan (Dataset Preloaded)

## Scope & Principles
Covers server‑side data initialization, variable mapping, integrity checks, KM, Cox PH, filters/exclusions, plot export, UI/API behavior, errors, performance, accessibility, and logging.

## Fixtures
- framingham_small.csv (optional local subset)
- Synthetic variants for zero‑events, all‑events‑t0, period3 lipids, smoking inconsistent, collinear, missing predictors

## Unit Tests (examples)
- dataset loaded on startup; /api/columns returns types and defaults
- default outcome mappings exist; override respected
- period‑3 lipids warning; smoking consistency flags

## KM Tests
- monotone non‑increasing survival; zero‑events & all‑t0 edges
- CI presence; labels/legend/title

## Cox Tests
- single & multiple predictors; categorical encoding and baseline reporting
- collinearity detection; non‑convergence handling
- filters for prevalent disease; period‑3 effect

## API/Export
- /api/km & /api/cox contract; /api/export_plot returns image bytes
- /health returns ok

## Performance
- KM ≤2s; Cox ≤5s

## Accessibility
- Keyboard navigation; ARIA labels present in UI
