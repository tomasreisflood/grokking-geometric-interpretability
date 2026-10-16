# Stress-Testing Geometric Interpretability Claims in Grokking

How does a transformer's representation move as it learns to generalise?
This project studies modular-addition grokking using Hodge decomposition of
activation displacements, repeated training runs, and correspondence controls.

**[Read the manuscript](papers/stress-testing-geometric-interpretability.pdf)**

## Main finding

Across eight training seeds and seven analysis settings, the difference between
coexact and exact motion fractions decreases from the transition to the
post-grokking phase in all 56 seed-by-setting comparisons. At the baseline
setting, the mean change is **−0.267**, with a seed-level 95% t interval of
**[−0.400, −0.135]**. The eight training seeds are the independent units.

This supports a relative shift towards exact motion. It does not establish
universal exact dominance or a causal mechanism for generalisation.

## Code map

| Stage | Entry point | Shared implementation |
|---|---|---|
| Configuration | Training and analysis scripts | [`config.py`](src/grokking_velocity_hodge/config.py) |
| Train and capture activations | [`01_train_reproducible.py`](reproducibility/Grokking/Training/01_train_reproducible.py) | TransformerLens |
| Decompose representational motion | [`01_velocity_hodge.py`](reproducibility/Grokking/Analysis/01_velocity_hodge.py) | [`runtime.py`](src/grokking_velocity_hodge/runtime.py), DiffusionGeometry |
| Test sensitivity and correspondence | [`11_hodge_robustness.py`](reproducibility/Grokking/Analysis/11_hodge_robustness.py) | [`robustness.py`](src/grokking_velocity_hodge/robustness.py) |
| Aggregate across training seeds | [`12_hodge_cross_seed_summary.py`](reproducibility/Grokking/Analysis/12_hodge_cross_seed_summary.py) | [`reporting.py`](src/grokking_velocity_hodge/reporting.py) |
| Calibrate on synthetic fields | [`01_synthetic_hodge.py`](reproducibility/Grokking/Validation/01_synthetic_hodge.py) | [`calibration.py`](src/grokking_velocity_hodge/calibration.py) |

The `reproducibility/` scripts import the installable package under `src/`.
Additional analyses cover effective dimension, diffusion operators, Fourier
diagnostics, and Bures–Wasserstein distances. Figures are in [`figures/`](figures/).

## Reproduce the reported result

Use Python 3.11 or newer. From the repository root:

```powershell
python -m pip install -e ".[dev]"
python reproducibility/Grokking/Analysis/12_hodge_cross_seed_summary.py
```

This verifies the bundled input manifest and regenerates the eight-seed
statistics, CSV summaries, and LaTeX table inputs. It does not require retraining
or downloading the large activation arrays.

Saved empirical records and training metadata are in
[`reproducibility/artifacts/eight_seed_hodge/`](reproducibility/artifacts/eight_seed_hodge/).
Generated outputs go below that directory and into `generated/`.

For training, install the optional dependencies:

```powershell
python -m pip install -e ".[training]"
python reproducibility/Grokking/Training/01_train_reproducible.py
```

See [`reproducibility/README.md`](reproducibility/README.md) for the full workflow,
eight-run sweep, environment overrides, and output locations.

## Validation

```powershell
python -m unittest discover -s reproducibility/tests -v
ruff check .
python reproducibility/Grokking/Pipelines/main_charts.py --dry-run
```

Tests include synthetic Hodge calibration, saved-result inference, and pipeline
checks. Model checkpoints and raw activations are excluded because of their size.

## Manuscript and provenance

The retained PDF is the submission manuscript dated **2 September 2026, 21:04**.
See [`papers/README.md`](papers/README.md) for its exact source filename and hash.
Its workshop formatting does not imply acceptance or publication.

The code and saved evidence derive from
[`tomasblood/stress-testing-geometric-interpretability`](https://github.com/tomasblood/stress-testing-geometric-interpretability)
at commit `b621d856a20f98170cf48cb9dadc4f7270bb1df2`. The original source and
manuscript history remain in that repository. This repository retains the MIT
licence and a focused set of code, results, tests, and figures.

Implementation detail: the training script feeds `[a, b]` and extracts MLP
activations at the final input position. It supplies no equals token; manuscript
references to an equals-token position should be read with this correction.

Numerical provenance and dependency pinning are documented in
[`reproducibility/PROVENANCE.md`](reproducibility/PROVENANCE.md).
