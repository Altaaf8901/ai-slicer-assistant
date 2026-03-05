from __future__ import annotations
import json, random, time
from .base import ModelProvider, ModelResult

class StubProvider(ModelProvider):
    def generate(self, *, prompt: str, model: str) -> ModelResult:
        t0 = time.perf_counter()

        material = "PLA" if "PLA" in prompt.upper() else "ABS" if "ABS" in prompt.upper() else "PETG"
        nozzle = 0.4

        candidate = {
            "material": material,
            "nozzle_mm": nozzle,
            "layer_height_mm": random.choice([0.2, 0.28, 0.45]),
            "print_speed_mm_s": random.choice([45, 60, 140]),
            "infill_percent": random.choice([15, 30, 110]),
            "supports": random.choice([True, False]),
            "bed_temp_c": random.choice([55, 90, 0]),
            "nozzle_temp_c": random.choice([205, 260, 195]),
            "notes": "provider:stub"
        }

        raw = json.dumps(candidate)
        latency_ms = int((time.perf_counter() - t0) * 1000)
        return ModelResult(raw_text=raw, latency_ms=latency_ms)
