from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from sqlalchemy import create_engine, text

def generate_report(db_path: str, out_path: str = "artifacts/reports/summary.md") -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", future=True)

    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM traces")).scalar_one()
        valid = conn.execute(text("SELECT COUNT(*) FROM traces WHERE valid = 1")).scalar_one()
        invalid = total - valid
        parse_fail = conn.execute(text("SELECT COUNT(*) FROM traces WHERE parsed_ok = 0")).scalar_one()

        rows = conn.execute(text("SELECT violations_json FROM traces WHERE valid = 0")).fetchall()
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
    lines.append(f"- Total runs: **{total}**")
    lines.append(f"- Valid: **{valid}**")
    lines.append(f"- Invalid: **{invalid}**")
    lines.append(f"- Parse failures: **{parse_fail}**")
    lines.append(f"- Validity rate: **{validity_rate:.2f}%**")
    lines.append("")
    lines.append("## Top failure modes (by validator message)")
    if not top:
        lines.append("- None 🎉")
    else:
        for msg, c in top:
            lines.append(f"- {c} × {msg}")

    content = "\n".join(lines) + "\n"
    Path(out_path).write_text(content, encoding="utf-8")
    return out_path
