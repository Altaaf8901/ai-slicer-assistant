# AI Slicer Assistant

Reliability evaluation harness for AI-generated 3D printing slicer configurations.

This project explores how to safely generate structured configurations from LLMs by combining:

- Prompt templates
- Structured parsing
- Schema validation
- Deterministic rule validators
- Retry/correction loops
- Telemetry logging
- Evaluation metrics

The goal is to simulate how production systems validate and repair LLM outputs.

---

## Project Architecture
ai-slicer-assistant
├── src/aislicer
│ ├── cli.py # Command line interface
│ ├── core
│ │ ├── normalize.py # Input normalization
│ │ ├── parse.py # JSON + schema parsing
│ │ ├── retry.py # Retry / correction loop
│ │ └── providers # Model providers (stub / future LLMs)
│ ├── eval
│ │ ├── evaluator.py # Evaluation runner
│ │ └── report.py # Metrics + report generation
│ ├── telemetry
│ │ └── storage.py # SQLite trace logging
│ └── tasks
│ └── slicer_v1 # Task definition
│ ├── schema.py
│ ├── validators.py
│ └── scenarios.jsonl

---

## Example Usage

Generate a config:
python -m aislicer run --material PLA --nozzle 0.4 --goal strength


Run evaluation:
python -m aislicer eval --n 5


Generate report:
python -m aislicer report


Example output:
Validity rate: 30%
Top failures:
parse_failed
layer height too high
ABS bed temperature too low

---

## Why This Project Exists

LLMs frequently generate outputs that are:

- syntactically invalid
- schema-invalid
- logically unsafe

This project demonstrates a **defensive architecture** that combines:

1. structured prompts  
2. deterministic validation  
3. automatic correction retries  
4. telemetry + evaluation  

This pattern is widely used in production LLM systems.

---

## Future Improvements

- Replace stub provider with real LLM API
- Add structured JSON schema prompting
- Add retry heuristics based on failure types
- Add benchmark metrics across model versions
