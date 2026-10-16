"""Run and persist the real DiffusionGeometry synthetic Hodge calibration."""

from grokking_velocity_hodge.calibration import run_synthetic_hodge_calibration
from grokking_velocity_hodge.provenance import verify_diffusion_geometry_provenance
from grokking_velocity_hodge.runtime import configure_grokking_runtime, write_json


def main() -> None:
    print(f"DiffusionGeometry provenance: {verify_diffusion_geometry_provenance()}")
    runtime = configure_grokking_runtime()
    output = runtime.result_dir("grokking_hodge_calibration") / "synthetic_hodge.json"
    calibration = run_synthetic_hodge_calibration()
    write_json(output, calibration)
    assert calibration["passed"], calibration["checks"]
    print(f"Synthetic Hodge calibration passed: {output}")


if __name__ == "__main__":
    main()
