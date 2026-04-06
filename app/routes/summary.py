from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core import oauth2
from app.database.db import get_db
from app import models

router = APIRouter(
    prefix="/summary",
    tags=["Financial Summary"]
)


# Total Income
@router.get("/income")
def total_income(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    total = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == "income"
    ).scalar()

    return {"total_income": total or 0}


# Total Expenses
@router.get("/expenses")
def total_expenses(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    total = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == "expense"
    ).scalar()

    return {"total_expenses": total or 0}


# Current Balance
@router.get("/balance")
def current_balance(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == "income"
    ).scalar() or 0

    expenses = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == "expense"
    ).scalar() or 0

    return {
        "total_income": income,
        "total_expenses": expenses,
        "current_balance": income - expenses
    }


# Category Wise Breakdown
@router.get("/category")
def category_breakdown(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    results = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount)
    ).group_by(models.Transaction.category).all()

    return [
        {"category": category, "total": total}
        for category, total in results
    ]


# Monthly Totals
@router.get("/monthly")
def monthly_totals(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    results = db.query(
        extract("year", models.Transaction.date).label("year"),
        extract("month", models.Transaction.date).label("month"),
        func.sum(models.Transaction.amount)
    ).group_by("year", "month").all()

    return [
        {
            "year": int(year),
            "month": int(month),
            "total": total
        }
        for year, month, total in results
    ]


# Recent Activity (last 5 transactions)
@router.get("/recent")
def recent_activity(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    transactions = db.query(models.Transaction).order_by(
        models.Transaction.date.desc()
    ).limit(5).all()

    return transactions