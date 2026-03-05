from __future__ import annotations
from pathlib import Path
from aislicer.core.normalize import Job


def build_prompt(job: Job, prompt_version: str = "v1") -> str:
    base = Path("src/aislicer/prompts") / prompt_version
    system = (base / "system.txt").read_text(encoding="utf-8")
    user_t = (base / "user_template.txt").read_text(encoding="utf-8")

    user = user_t.format(material=job.material, nozzle_mm=job.nozzle_mm, goal=job.goal)
    return f"{system}\n\n{user}\n"
