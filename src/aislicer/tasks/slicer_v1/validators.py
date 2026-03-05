from typing import List
from .schema import SlicerConfigV1


def validate_config(cfg: SlicerConfigV1) -> List[str]:
    issues: List[str] = []

    if cfg.layer_height_mm > cfg.nozzle_mm * 0.8:
        issues.append(
            "layer_height_mm too high for nozzle diameter (risk of poor extrusion)."
        )

    mat = cfg.material.strip().upper()
    if mat == "PLA":
        if not (180 <= cfg.nozzle_temp_c <= 230):
            issues.append("PLA nozzle_temp_c outside typical range (180–230).")
        if not (0 <= cfg.bed_temp_c <= 70):
            issues.append("PLA bed_temp_c outside typical range (0–70).")

    if mat == "ABS":
        if cfg.bed_temp_c < 80:
            issues.append("ABS bed_temp_c likely too low (<80).")

    if cfg.print_speed_mm_s > 120 and cfg.layer_height_mm < 0.15:
        issues.append("High speed + small layer height may reduce print quality.")

    return issues
