from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from sqlalchemy import Boolean, Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Trace(Base):
    __tablename__ = "traces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_utc = Column(String, nullable=False)
    experiment = Column(String, nullable=False)

    task = Column(String, nullable=False)
    scenario_id = Column(String, nullable=False)

    model = Column(String, nullable=False)
    prompt_version = Column(String, nullable=False)

    prompt_text = Column(Text, nullable=False)
    raw_response_text = Column(Text, nullable=False)

    parsed_ok = Column(Boolean, nullable=False)
    parse_error = Column(Text, nullable=False)

    output_json = Column(Text, nullable=False)
    valid = Column(Boolean, nullable=False)
    violations_json = Column(Text, nullable=False)

    latency_ms = Column(Integer, nullable=False)
    retries = Column(Integer, nullable=False)


@dataclass(frozen=True)
class TraceEvent:
    task: str
    scenario_id: str
    model: str
    prompt_version: str
    prompt_text: str
    raw_response_text: str
    parsed_ok: bool
    parse_error: str
    output_obj: Dict[str, Any]
    valid: bool
    violations: List[str]
    latency_ms: int
    retries: int
    experiment: str


class TelemetryStore:
    def __init__(self, db_path: str = "artifacts/telemetry.sqlite"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{db_path}", future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

    def write_trace(self, ev: TraceEvent) -> None:
        created_utc = datetime.now(timezone.utc).isoformat()

        row = Trace(
            created_utc=created_utc,
            experiment=ev.experiment,
            task=ev.task,
            scenario_id=ev.scenario_id,
            model=ev.model,
            prompt_version=ev.prompt_version,
            prompt_text=ev.prompt_text,
            raw_response_text=ev.raw_response_text,
            parsed_ok=ev.parsed_ok,
            parse_error=ev.parse_error,
            output_json=json.dumps(ev.output_obj, separators=(",", ":")),
            valid=ev.valid,
            violations_json=json.dumps(ev.violations, separators=(",", ":")),
            latency_ms=int(ev.latency_ms),
            retries=int(ev.retries),
        )

        with self.Session() as s:
            s.add(row)
            s.commit()
