from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database.db import get_db
from app import models, schemas
from app.core import oauth2

router = APIRouter(
    prefix="/transactions", 
    tags=["Transactions"]
    )

@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(transaction: schemas.TransactionCreate,db: Session = Depends(get_db), 
                       current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_transaction = models.Transaction(**transaction.dict())

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@router.get("/", response_model=List[schemas.TransactionResponse])
def get_transactions(db: Session = Depends(get_db),
                     category: Optional[str] = None, 
                     type: Optional[str] = None,
                     start_date: Optional[date] = None,
                     end_date: Optional[date] = None,
                     current_user: models.User = Depends(oauth2.get_current_user)):

    transactions = db.query(models.Transaction)

    if category:
        transactions = transactions.filter(models.Transaction.category == category)
    if type:
        transactions = transactions.filter(models.Transaction.type == type)
    if start_date:
        transactions = transactions.filter(models.Transaction.date >= start_date)
    if end_date:
        transactions = transactions.filter(models.Transaction.date <= end_date)

    transactions = transactions.all()

    return transactions


@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(transaction_id: int, updated_data: schemas.TransactionUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in updated_data.dict().items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_admin)):

    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted"}