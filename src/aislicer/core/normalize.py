from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    material: str
    nozzle_mm: float
    goal: str


def normalize_inputs(material: str, nozzle: float, goal: str) -> Job:
    return Job(
        material=material.strip(), nozzle_mm=float(nozzle), goal=goal.strip().lower()
    )
