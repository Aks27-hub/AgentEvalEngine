# AgentEval-Engine 🛡️🤖
> *Production Autonomous Agent Testing, Benchmarking & Regression Suite*

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/pytest-compatible-orange.svg)](https://docs.pytest.org/)
[![LLM Judge](https://img.shields.io/badge/Judge-Gemini%203.6%20Flash-green.svg)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Production-Ready-success.svg)]()

`AgentEval-Engine` is a lightweight, rigorous testing framework built to solve the hardest problem in production AI engineering: **ensuring autonomous multi-step agents execute complex enterprise tasks without side effects, state drift, or safety violations.**

Inspired by modern software testing frameworks (like Pytest and VCR.py), this engine validates agents across three critical pillars: **Deterministic State Accuracy**, **Tool Efficiency**, and **Reasoning Safety**.

---

## 🏗️ System Architecture

```text
                     ┌───────────────────────────┐
                     │   Evaluation Controller   │
                     └─────────────┬─────────────┘
                                   │
             ┌─────────────────────┴─────────────────────┐
             ▼                                           ▼
┌───────────────────────────┐               ┌───────────────────────────┐
│     Agent Execution       │               │    Mock Environment       │
│   (Recorded & Traced)     │               │   (Deterministic State)   │
└────────────┬──────────────┘               └────────────┬──────────────┘
             │                                           │
             └─────────────────────┬─────────────────────┘
                                   ▼
                     ┌───────────────────────────┐
                     │    Evaluator Pipeline     │
                     │ - Deterministic State Diff│
                     │ - LLM-as-a-Judge Reasoning│
                     │ - Tool Protocol Inspector │
                     └─────────────┬─────────────┘
                                   ▼
                     ┌───────────────────────────┐
                     │    HTML / CLI Reporter    │
                     └───────────────────────────┘
```

## ✨ Key Differentiators & Features
1. Stateful Mock Sandbox (sandbox.py): Simulates complex backend systems (CRM/ERP workflows) with Pydantic data validation and instant baseline resets before every test run.

2. Deterministic State Diff Evaluator (state_eval.py): Verifies that agents reached desired system mutations without causing collateral damage (e.g., preventing accidental zeroing out of customer balances).

3. LLM-as-a-Judge Reasoning (judge.py): Leverages Gemini to evaluate qualitative dimensions like tool efficiency (looping/redundancy checks) and safety protocols.

4. VCR-Style Replay Mode (replay.py): Caches tool outputs and LLM judge responses into cassettes, allowing test suites to run instantly and cost-free in CI/CD pipelines.

5. Executive Dashboard & HTML Reporter: Renders gorgeous terminal dashboards using Rich and auto-generates a standalone report.html file for stakeholder review.

## 📂 Project Structure
agent-eval-engine/

├── sandbox.py             # Stateful mock backend

├── tracer.py              # Trace collector structures

├── replay.py              # VCR cassette caching system

├── cli.py                 # Rich CLI dashboard & HTML generator

├── runner.py              # Core test suite orchestrator

├── evaluators/

│   ├── __init__.py

│   ├── state_eval.py      # Deterministic state diff engine

│   └── judge.py           # Gemini LLM-as-a-Judge evaluator

├── test_cases/

│   ├── crm_update.yaml    # Declarative YAML test case 1

│   └── crm_complex_workflow.yaml # Advanced multi-step test case 2

└── test_agent.py          # Pytest integration wrapper

## 🚀 Quickstart Guide
1. Installation

Clone the repository and install dependencies:

```Bash
git clone https://github.com/Aks27-hub/AgentEvalEngine.git
cd AgentEvalEngine
pip install pytest pyyaml pydantic rich google-genai
```

2. Set Your API Key

Configure your Gemini API key for LLM-as-a-Judge evaluations:

PowerShell:
```Bash
$env:GEMINI_API_KEY="your-gemini-api-key"
```

Linux / Mac:
```Bash
export GEMINI_API_KEY="your-gemini-api-key"
```

3. Run the CLI Dashboard

Execute the full evaluation suite and generate your interactive terminal and HTML reports:

```Bash
python cli.py
(To run using cached mock responses in CI/CD mode: python cli.py --replay)
```

4. Run via Pytest (CI/CD Integration)

```Bash
pytest -v
```
