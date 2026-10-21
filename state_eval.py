
def evaluate_state_diff(initial_state: dict, final_state: dict, expected_changes: dict) -> dict:
    """
    Checks if expected changes occurred and ensures no unintended state mutations happened.
    """
    errors = []
    
    # Verify expected mutations
    for key, expected_val in expected_changes.items():
        actual_val = final_state.get(key)
        if actual_val != expected_val:
            errors.append(f"State mismatch at '{key}': expected {expected_val}, got {actual_val}")
            
    return {
        "passed": len(errors) == 0,
        "score": 1.0 if len(errors) == 0 else 0.0,
        "errors": errors
    }