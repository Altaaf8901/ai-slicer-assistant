import typer
from rich import print

from aislicer.core.normalize import normalize_inputs
from aislicer.core.prompting import build_prompt
from aislicer.core.providers.stub import StubProvider
from aislicer.core.parse import parse_slicer_config
from aislicer.tasks.slicer_v1.validators import validate_config

from aislicer.eval.evaluator import run_eval
from aislicer.eval.report import generate_report

app = typer.Typer(add_completion=False)

@app.command()
def run(
    material: str = typer.Option(...),
    nozzle: float = typer.Option(0.4),
    goal: str = typer.Option("balanced"),
    model: str = typer.Option("stub"),
    prompt_version: str = typer.Option("v1"),
):
    job = normalize_inputs(material=material, nozzle=nozzle, goal=goal)
    prompt_text = build_prompt(job, prompt_version=prompt_version)

    provider = StubProvider()
    res = provider.generate(prompt=prompt_text, model=model)

    cfg, parsed_ok, parse_error = parse_slicer_config(res.raw_text)
    if not parsed_ok or cfg is None:
        print("[bold red]Parse failed:[/bold red]", parse_error)
        print("Raw:", res.raw_text)
        raise typer.Exit(code=2)

    issues = validate_config(cfg)
    print("[bold]Generated config:[/bold]")
    print(cfg.model_dump())

    if issues:
        print("\n[bold red]Validation issues:[/bold red]")
        for i, msg in enumerate(issues, 1):
            print(f"{i}. {msg}")
        raise typer.Exit(code=2)

    print("\n[bold green]Config passed validation.[/bold green]")

@app.command()
def eval(
    n: int = typer.Option(5),
    model: str = typer.Option("stub"),
    prompt_version: str = typer.Option("v1"),
    db: str = typer.Option("artifacts/telemetry.sqlite"),
):
    total, valid = run_eval(
        task="slicer_v1",
        scenarios_path="src/aislicer/tasks/slicer_v1/scenarios.jsonl",
        model=model,
        prompt_version=prompt_version,
        limit=n,
        db_path=db,
    )
    print(f"[bold]Eval complete[/bold] — valid {valid}/{total}. Traces saved to: {db}")

@app.command()
def report(
    db: str = typer.Option("artifacts/telemetry.sqlite"),
    out: str = typer.Option("artifacts/reports/summary.md"),
):
    p = generate_report(db_path=db, out_path=out)
    print(f"[bold green]Report written:[/bold green] {p}")

if __name__ == "__main__":
    app()
