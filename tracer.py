from dataclasses import dataclass, field
import time
from typing import List, Any

@dataclass
class ToolCallTrace:
    tool_name: str
    args: dict
    output: Any
    timestamp: float

@dataclass
class AgentRunTrace:
    test_id: str
    prompt: str
    tool_calls: List[ToolCallTrace] = field(default_factory=list)
    initial_state: dict = field(default_factory=dict)
    final_state: dict = field(default_factory=dict)
    total_tokens: int = 0
    duration: float = 0.0
    final_response: str = ""