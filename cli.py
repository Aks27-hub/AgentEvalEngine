import glob
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from runner import run_test_case
from replay import load_cassette, save_cassette

console = Console()

def generate_html_report(results: list, html_path="report.html"):
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AgentEval-Engine Executive Report</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }}
            .card {{ background: #1e293b; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #334155; }}
            .pass {{ color: #4ade80; font-weight: bold; }}
            .fail {{ color: #f87171; font-weight: bold; }}
            h1 {{ color: #38bdf8; }}
        </style>
    </head>
    <body>
        <h1>AgentEval-Engine Benchmark Report</h1>
        <p>Summary: <strong>{passed_count}/{total_count}</strong> Tests Passed</p>
    """
    
    for r in results:
        status_class = "pass" if r["passed"] else "fail"
        status_text = "PASS" if r["passed"] else "FAIL"
        html_content += f"""
        <div class="card">
            <h3>{r['test_id']} - <span class="{status_class}">{status_text}</span></h3>
            <p><strong>State Errors:</strong> {r['state_result'].get('errors', [])}</p>
            <p><strong>Constraint Errors:</strong> {r['constraint_errors']}</p>
            <p><strong>Judge Reasoning:</strong> {r.get('judge_result', {}).get('reasoning', 'N/A')}</p>
        </div>
        """
    html_content += "</body></html>"
    
    with open(html_path, "w") as f:
        f.write(html_content)

def main(use_replay: bool = False):
    console.print(Panel.fit("[bold cyan]AgentEval-Engine[/bold cyan]\nProduction Autonomous Agent Benchmarking Suite", border_style="cyan"))
    
    yaml_files = glob.glob("test_cases/*.yaml")
    results = []
    
    table = Table(title="Test Suite Execution Results", show_header=True, header_style="bold magenta")
    table.add_column("Test ID", style="dim", width=30)
    table.add_column("Status", justify="center")
    table.add_column("Efficiency Score", justify="center")
    table.add_column("Safety Score", justify="center")
    table.add_column("Details")
    
    for yaml_path in yaml_files:
        # Quick load YAML to check test_id for replay
        import yaml
        with open(yaml_path, "r") as f:
            cfg = yaml.safe_load(f)
        test_id = cfg.get("test_id")
        
        result = None
        if use_replay:
            result = load_cassette(test_id)
            
        if not result:
            result = run_test_case(yaml_path)
            if use_replay:
                save_cassette(test_id, result)
                
        results.append(result)
        
        passed = result["passed"]
        status_str = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        judge = result.get("judge_result", {})
        eff = str(judge.get("efficiency_score", "N/A"))
        safe = str(judge.get("safety_score", "N/A"))
        details = "OK" if passed else str(result.get("state_result", {}).get("errors", ["Failed constraints"]))
        
        table.add_row(test_id, status_str, eff, safe, str(details))
        
    console.print(table)
    generate_html_report(results)
    console.print("\n[bold green]✔ Generated standalone report at 'report.html'![/bold green]")

if __name__ == "__main__":
    import sys
    replay_flag = "--replay" in sys.argv
    main(use_replay=replay_flag)