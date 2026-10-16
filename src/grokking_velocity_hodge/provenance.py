"""Helpers for auditing cached and freshly reproduced BW series."""

import json
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

import numpy as np

from .summary import summarise_transition_series

EXPECTED_DIFFUSION_GEOMETRY_COMMIT = "f5dc795557d07b32795c0bb6bedf465246d999eb"


def verify_diffusion_geometry_provenance() -> dict[str, str]:
    """Fail before an empirical DG analysis if the installed VCS revision is not pinned."""
    try:
        package = distribution("diffusion-geometry")
    except PackageNotFoundError as error:
        raise RuntimeError("diffusion-geometry is not installed") from error

    direct_url_text = package.read_text("direct_url.json")
    if not direct_url_text:
        raise RuntimeError(
            "Cannot verify the diffusion-geometry revision: direct_url.json is missing. "
            'Reinstall the project with python -m pip install --force-reinstall -e ".[dev]".'
        )
    direct_url = json.loads(direct_url_text)
    commit = str(direct_url.get("vcs_info", {}).get("commit_id", ""))
    if commit != EXPECTED_DIFFUSION_GEOMETRY_COMMIT:
        raise RuntimeError(
            "Wrong diffusion-geometry revision: "
            f"installed {commit or 'unknown'}, expected {EXPECTED_DIFFUSION_GEOMETRY_COMMIT}. "
            'Reinstall the project with python -m pip install --force-reinstall -e ".[dev]".'
        )
    return {"distribution": package.metadata["Name"], "commit": commit}


def file_sha256(path: str | Path) -> str:
    return sha256(Path(path).read_bytes()).hexdigest()


def load_bw_series(path: str | Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    return payload["bw_distances_consecutive"]


def compare_bw_files(cached_path: str | Path, rerun_path: str | Path) -> dict:
    cached = load_bw_series(cached_path)
    rerun = load_bw_series(rerun_path)
    cached_midpoints = np.asarray(cached["midpoint_epochs"], dtype=float)
    rerun_midpoints = np.asarray(rerun["midpoint_epochs"], dtype=float)
    cached_distances = np.asarray(cached["distances"], dtype=float)
    rerun_distances = np.asarray(rerun["distances"], dtype=float)

    same_grid = np.array_equal(cached_midpoints, rerun_midpoints)
    if cached_distances.shape != rerun_distances.shape:
        max_difference = None
    else:
        max_difference = float(np.max(np.abs(cached_distances - rerun_distances)))

    cached_summary = summarise_transition_series(cached_midpoints, cached_distances)
    rerun_summary = summarise_transition_series(rerun_midpoints, rerun_distances)
    cached_ratio = cached_summary["transition_peak_over_post_mean"]
    rerun_ratio = rerun_summary["transition_peak_over_post_mean"]
    ratio_difference = (
        abs(float(cached_ratio) - float(rerun_ratio))
        if cached_ratio is not None and rerun_ratio is not None
        else None
    )
    cached_transition_exceeds_post = cached_ratio is not None and float(cached_ratio) > 1.0
    rerun_transition_exceeds_post = rerun_ratio is not None and float(rerun_ratio) > 1.0
    numerically_stable = same_grid and ratio_difference is not None and ratio_difference <= 0.02
    conclusion_stable = same_grid and cached_transition_exceeds_post and rerun_transition_exceeds_post

    return {
        "cached": {"path": str(cached_path), "sha256": file_sha256(cached_path), "summary": cached_summary},
        "rerun": {"path": str(rerun_path), "sha256": file_sha256(rerun_path), "summary": rerun_summary},
        "same_midpoint_grid": same_grid,
        "series_exactly_equal": same_grid and np.array_equal(cached_distances, rerun_distances),
        "max_absolute_distance_difference": max_difference,
        "transition_peak_ratio_difference": ratio_difference,
        "transition_peak_exceeds_post_mean": {
            "cached": cached_transition_exceeds_post,
            "rerun": rerun_transition_exceeds_post,
        },
        "numerically_stable": numerically_stable,
        "conclusion_stable": conclusion_stable,
    }
