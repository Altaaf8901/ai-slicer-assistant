from __future__ import annotations

import time
from openai import OpenAI

from .base import ModelProvider, ModelResult


class OpenAIProvider(ModelProvider):
    def __init__(self) -> None:
        self.client = OpenAI()

    def generate(self, *, prompt: str, model: str) -> ModelResult:
        t0 = time.perf_counter()
        resp = self.client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
            text={"format": {"type": "json_object"}},
        from __future__ import annotations

import time
from openai import OpenAI

from .base import ModelProvider, ModelResult


class OpenAIProvider(ModelProvider):
    def __init__(self) -> None:
        self.client = OpenAI()

    def generate(self, *, prompt: str, model: str) -> ModelResult:
        t0 = time.perf_counter()

        resp = self.client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
            text={"format": {"type": "json_object"}},
        )

        latency_ms = int((time.perf_counter() - t0) * 1000)
        return ModelResult(raw_text=resp.output_text, latency_ms=latency_ms))
        latency_ms = int((time.perf_counter() - t0) * 1000)
from __future__ import annotations

import time
from openai import OpenAI

from .base import ModelProvider, ModelResult


class OpenAIProvider(ModelProvider):
    def __init__(self) -> None:
        self.client = OpenAI()

    def generate(self, *, prompt: str, model: str) -> ModelResult:
        t0 = time.perf_counter()

        resp = self.client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "slicer_settings",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "layer_height": {"type": "number"},
                            "print_speed": {"type": "number"},
                            "nozzle_temp": {"type": "number"},
                            "bed_temp": {"type": "number"},
                            "fan_speed": {"type": "number"},
                            "notes": {"type": "string"},
                        },
                        "required": [
                            "layer_height",
                            "print_speed",
                            "nozzle_temp",
                            "bed_temp",
                            "fan_speed",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
        )

        latency_ms = int((time.perf_counter() - t0) * 1000)

        return ModelResult(
            raw_text=resp.output_text,
            latency_ms=latency_ms,
        )        return ModelResult(raw_text=resp.output_text, latency_ms=latency_ms)
