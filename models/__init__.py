from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from database import Base


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    type = Column(String(3))
    amount = Column(Integer)
    description = Column(String(250))

    def __init__(self, date, type, amount, description):
        self.date = date
        self.type = type
        self.amount = amount
        self.description = description

    def __repr__(self):
        return {
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "amount": self.amount,
            "description": self.description
        }

    @property
    def serialize(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%d-%m-%Y"),
            "type": self.type,
            "amount": str(self.amount),
            "description": self.description
        }

    @classmethod
    def get_saldo(cls, end_date=None):
        if end_date is None:
            total = 0
            for t in cls.query.all():
                total += t.amount
            return "%.2f" % total
        else:
            total = 0
            for t in cls.query.filter(Transaction.date < end_date):
                total += t.amount
            return "%.2f" % total


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    color = Column(String(10))

    def __init__(self, name, color):
        self.name = name
        self.color = color


class LinkTagTransaction(Base):
    __tablename__ = 'linktagtransaction'
    id = Column(Integer, primary_key=True)
    id_tag = Column(Integer, ForeignKey('tag.id'))
    id_transaction = Column(Integer, ForeignKey('transaction.id'))
