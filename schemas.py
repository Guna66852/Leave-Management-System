from pydantic import BaseModel
from datetime import date

class EmployeeCreate(BaseModel):
    name: str
    email: str
    employee_id:int


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str