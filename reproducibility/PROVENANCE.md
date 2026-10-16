# Numerical provenance

The historical canonical BW cache and the current source are not
byte-identical. Two changes are documented: an earlier source-export/refactor
difference and a later fix that makes the requested `k` nearest neighbours mean
`k` non-self neighbours. The manuscript uses the current, corrected output.

- Historical cache SHA-256: `dfc367293485b45e2e0f65b8589183a45732e0f70995d91c95eba9ebb57c86fe`
- Current corrected output SHA-256 (2026-09-01 clean rerun): `f635b1c861a90a82c4ff8740cc5cd07e480bdfb7be0b2e3547e0890c3191d743`
- Historical initial / transition peak / post mean: `7.656752 / 1.624915 / 0.531719`
- Current initial / transition peak / post mean: `7.335185 / 1.646549 / 0.564001`
- Historical transition-peak/post mean ratio: `3.055966`
- Current transition-peak/post mean ratio: `2.919409`
- Maximum absolute series difference: `0.865010`

The numerical values are therefore not interchangeable. Both versions support
the narrower qualitative conclusion that the transition peak exceeds the
post-grokking mean, while all manuscript point estimates must be read from the
current corrected output. The provenance verifier reports numerical stability
and conclusion stability separately so that numeric drift cannot be mistaken
for exact reproduction.

Audit two files with:

```powershell
python reproducibility/Grokking/Validation/02_verify_bw_provenance.py `
  --cached path/to/bw_geodesic_results.json `
  --rerun path/to/resolvent_bw_results.json `
  --output path/to/provenance_report.json
```

## DiffusionGeometry revision and numerical environment

The empirical Hodge and circular-coordinate scripts require the exact
DiffusionGeometry Git revision pinned in `pyproject.toml`:
`f5dc795557d07b32795c0bb6bedf465246d999eb`. They now fail before analysis if
the installed distribution's `direct_url.json` records any other revision.
This check matters because the same package version label can refer to
different Git checkouts.

The 2026-09-01 clean audit used Python 3.14.2, NumPy 2.4.1, SciPy 1.17.0,
scikit-learn 1.8.0, Matplotlib 3.10.8, and the pinned DiffusionGeometry
revision. The exact single-run pre-grokking component fractions showed modest
numerical drift from the archived figure under this newer scientific stack;
the transition/post ordering and the paper's primary eight-seed directional
claim were unchanged. For that reason the manuscript treats the short
pre-grokking fractions as descriptive and bases inference on the checksummed
eight-seed artifacts below.

## Eight-seed Hodge evidence

The completed per-seed Hodge records and corresponding training histories are
stored in `reproducibility/artifacts/eight_seed_hodge`. Their source execution
metadata are embedded in each JSON file, and their SHA-256 digests are recorded
in `remote_artifact_manifest_8seed.json`. Regenerate the cross-seed statistics,
CSV audit tables, LaTeX inputs, and a new output manifest with:

```powershell
python reproducibility/Grokking/Analysis/12_hodge_cross_seed_summary.py
```

The report validates the bundled files against this manifest, then validates
record uniqueness, finiteness, and component sums before calculating results.
It also validates the exact seven-setting one-at-a-time grid, equal record
counts per setting, and that permutation records occur only at the baseline
setting. The merged per-seed JSON files retain `experiment_config.knn = 10`
from one isolated execution batch; this top-level field is not the setting for
all records. The per-record `(pca_dim, knn, n_basis)` fields and the top-level
`settings` array are authoritative, include the `(10, 15, 50)` baseline, and
are what the reporting code validates and aggregates.
The permutation null contains 288 paired records: one
separately drawn destination permutation for each of eight training seeds, four probe subsets,
and nine checkpoint pairs at the baseline parameter setting.
