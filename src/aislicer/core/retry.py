from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

from aislicer.core.providers.base import ModelProvider, ModelResult
from aislicer.core.parse import parse_slicer_config
from aislicer.tasks.slicer_v1.validators import validate_config

@dataclass(frozen=True)
class RunOutcome:
    raw_text: str
    latency_ms: int
    retries: int
    parsed_ok: bool
    parse_error: str
    violations: List[str]
    valid: bool
    output_obj: dict

def run_with_retries(
    *,
    provider: ModelProvider,
    model: str,
    base_prompt: str,
    max_retries: int = 2,
) -> RunOutcome:
    prompt = base_prompt
    retries = 0
    total_latency = 0

    last_raw = ""
    last_parse_error = ""
    last_violations: List[str] = []
    last_output: dict = {}
    last_parsed_ok = False
    last_valid = False

    while True:
        res: ModelResult = provider.generate(prompt=prompt, model=model)
        total_latency += res.latency_ms
        last_raw = res.raw_text

        cfg, parsed_ok, parse_error = parse_slicer_config(res.raw_text)
        last_parsed_ok = parsed_ok
        last_parse_error = parse_error

        if not parsed_ok or cfg is None:
            last_valid = False
            last_violations = [parse_error or "parse_failed"]
            last_output = {}

            if retries >= max_retries:
                break

            retries += 1
            # “Correction” prompt: tighten the instruction
            prompt = (
                base_prompt
                + "\n\nCORRECTION:\nReturn ONLY valid JSON. Ensure ALL required fields exist and match the schema types and ranges.\n"
            )
            continue

        # Rule validation
        last_output = cfg.model_dump()
        violations = validate_config(cfg)
        last_violations = violations
        if not violations:
            last_valid = True
            break

        if retries >= max_retries:
            last_valid = False
            break

        retries += 1
        prompt = (
            base_prompt
            + "\n\nCORRECTION:\nFix the following issues and return corrected JSON only:\n- "
            + "\n- ".join(violations)
            + "\n"
        )

    return RunOutcome(
        raw_text=last_raw,
        latency_ms=total_latency,
        retries=retries,
        parsed_ok=last_parsed_ok,
        parse_error=last_parse_error,
        violations=last_violations,
        valid=last_valid,
        output_obj=last_output,
    )
