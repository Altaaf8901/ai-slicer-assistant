from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from sqlalchemy import create_engine, text


def generate_report(
    db_path: str,
    out_path: str = "artifacts/reports/summary.md",
    experiment: str | None = None,
) -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(f"sqlite:///{db_path}", future=True)

    cond = "1=1"
    params: Dict[str, str] = {}

    if experiment:
        cond = "experiment = :experiment"
        params = {"experiment": experiment}

    with engine.connect() as conn:
        total = conn.execute(
            text(f"SELECT COUNT(*) FROM traces WHERE {cond}"), params
        ).scalar_one()

        valid = conn.execute(
            text(f"SELECT COUNT(*) FROM traces WHERE {cond} AND valid = 1"), params
        ).scalar_one()

        invalid = total - valid

        parse_fail = conn.execute(
            text(f"SELECT COUNT(*) FROM traces WHERE {cond} AND parsed_ok = 0"), params
        ).scalar_one()

        rows = conn.execute(
            text(f"SELECT violations_json FROM traces WHERE {cond} AND valid = 0"),
            params,
        ).fetchall()

    counts: Dict[str, int] = {}

    for (vj,) in rows:
        try:
            violations = json.loads(vj)
        except Exception:
            violations = ["<unparseable violations_json>"]

        for v in violations:
            counts[v] = counts.get(v, 0) + 1

    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

    validity_rate = (valid / total * 100.0) if total else 0.0

    lines = []
    lines.append("# AI Slicer Assistant — Eval Summary")
    lines.append("")

    if experiment:
        lines.append(f"- Experiment: **{experiment}**")

    lines.append(f"- Total runs: **{total}**")
    lines.append(f"- Valid: **{valid}**")
    lines.append(f"- Invalid: **{invalid}**")
    lines.append(f"- Parse failures: **{parse_fail}**")
    lines.append(f"- Validity rate: **{validity_rate:.2f}%**")
    lines.append("")
    lines.append("## Top failure modes (by validator message)")

    for msg, n in top:
        lines.append(f"- {n} × {msg}")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")

    return out_path
