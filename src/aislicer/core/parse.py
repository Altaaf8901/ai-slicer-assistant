from __future__ import annotations
import json
from typing import Tuple, Optional
from pydantic import ValidationError
from aislicer.tasks.slicer_v1.schema import SlicerConfigV1

def parse_slicer_config(raw_text: str) -> Tuple[Optional[SlicerConfigV1], bool, str]:
    try:
        obj = json.loads(raw_text)
    except Exception as e:
        return None, False, f"json_load_error: {e}"

    try:
        cfg = SlicerConfigV1.model_validate(obj)
        return cfg, True, ""
    except ValidationError as e:
        return None, False, f"schema_validation_error: {e}"
