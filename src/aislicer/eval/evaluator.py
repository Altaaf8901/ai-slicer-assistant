
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from aislicer.core.normalize import normalize_inputs
from aislicer.core.prompting import build_prompt
from aislicer.core.providers.stub import StubProvider
from aislicer.core.retry import run_with_retries

from aislicer.telemetry.storage import TelemetryStore, TraceEvent


def load_scenarios(jsonl_path: str) -> List[Dict[str, Any]]:
    p = Path(jsonl_path)
    scenarios: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        scenarios.append(json.loads(line))
    return scenarios


def run_eval(
    *,
    task: str,
    scenarios_path: str,
    model: str,
    prompt_version: str,
    limit: int,
    db_path: str,
) -> Tuple[int, int]:
    store = TelemetryStore(db_path=db_path)
    provider = StubProvider()

    scenarios = load_scenarios(scenarios_path)[:limit]

    total = 0
    valid_count = 0

    for s in scenarios:
        scenario_id = s["scenario_id"]
        inp = s["input"]

        job = normalize_inputs(material=inp["material"], nozzle=inp["nozzle"], goal=inp["goal"])
        prompt_text = build_prompt(job, prompt_version=prompt_version)

        out = run_with_retries(
            provider=provider,
            model=model,
            base_prompt=prompt_text,
            max_retries=2,
        )

        store.write_trace(
            TraceEvent(
                task=task,
                scenario_id=scenario_id,
                model=model,
                prompt_version=prompt_version,
                prompt_text=prompt_text,
                raw_response_text=out.raw_text,
                parsed_ok=out.parsed_ok,
                parse_error=out.parse_error,
                output_obj=out.output_obj,
                valid=out.valid,
                violations=out.violations,
                latency_ms=out.latency_ms,
                retries=out.retries,
            )
        )

        total += 1
        if out.valid:
            valid_count += 1

    return total, valid_count
