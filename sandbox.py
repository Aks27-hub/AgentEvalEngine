from pydantic import BaseModel
from typing import Dict, List

class Customer(BaseModel):
    id: str
    name: str
    status: str
    balance: float

class MockDatabase:
    def __init__(self):
        self.reset()

    def reset(self):
        # Resets the database to its initial state
        self.customers: Dict[str, Customer] = {
            "CUST-001": Customer(id="CUST-001", name="Alice", status="active", balance=500.0),
            "CUST-002": Customer(id="CUST-002", name="Bob", status="pending", balance=50.0),
            "CUST-003": Customer(id="CUST-003", name="Charlie", status="active", balance=75.0),
        }
        self.audit_logs: List[str] = []

    def get_customer(self, cust_id: str) -> dict:
        if cust_id in self.customers:
            self.audit_logs.append(f"Inspected customer {cust_id}")
            return {"success": True, "customer": self.customers[cust_id].model_dump()}
        return {"success": False, "error": "Customer not found"}

    def update_customer_status(self, cust_id: str, new_status: str):
        if cust_id in self.customers:
            self.customers[cust_id].status = new_status
            self.audit_logs.append(f"Updated {cust_id} status to {new_status}")
            return {"success": True, "customer": self.customers[cust_id].model_dump()}
        return {"success": False, "error": "Customer not found"}

    def get_snapshot(self) -> dict:
        snapshot = {k: v.model_dump() for k, v in self.customers.items()}
        snapshot["_audit_logs"] = self.audit_logs.copy()
        return snapshot
