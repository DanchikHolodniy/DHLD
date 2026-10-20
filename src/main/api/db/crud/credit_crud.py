from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit:
        return db.query(Credit).filter(Credit.account_id == account_id).first()

    @staticmethod
    def get_credit_by_credit_id(db: Session, id: int) -> Credit:
        return db.query(Credit).filter(Credit.id == id).first()
