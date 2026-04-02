from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String)
    date = Column(Date)
    notes = Column(String)