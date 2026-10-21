import glob
import pytest
from runner import run_test_case

# Automatically discover all test configurations in test_cases/
yaml_files = glob.glob("test_cases/*.yaml")

@pytest.mark.parametrize("yaml_path", yaml_files)
def test_agent_suite(yaml_path):
    result = run_test_case(yaml_path)
    
    # Format clear diagnostic error outputs on test failure
    assert result["passed"], (
        f"\n[FAIL] Test ID: {result['test_id']}\n"
        f"  - State Errors: {result['state_result'].get('errors', [])}\n"
        f"  - Constraint Errors: {result['constraint_errors']}"
        f" - Judge result: {result.get('judge_result', {})}"
    )