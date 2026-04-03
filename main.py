from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees")
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    emp = models.Employee(
        name=employee.name,
        email=employee.email,
        employee_id=employee.employee_id
    )

    db.add(emp)
    db.commit()
    db.refresh(emp)

    return emp


@app.post("/leave/apply")
def apply_leave(leave: schemas.LeaveCreate, db: Session = Depends(get_db)):

    if leave.start_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot apply leave in past")

    leave_request = models.LeaveRequest(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending"
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


@app.get("/leave")
def get_leaves(db: Session = Depends(get_db)):
    return db.query(models.LeaveRequest).all()


@app.put("/leave/{leave_id}/approve")
def approve_leave(leave_id: int, db: Session = Depends(get_db)):

    leave = db.query(models.LeaveRequest).get(leave_id)

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = "Approved"

    db.commit()

    return leave


@app.put("/leave/{leave_id}/reject")
def reject_leave(leave_id: int, db: Session = Depends(get_db)):

    leave = db.query(models.LeaveRequest).get(leave_id)

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = "Rejected"

    db.commit()

    return leave