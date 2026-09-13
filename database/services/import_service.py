from sqlalchemy.orm import Session

from database.repositories.account_repository import AccountRepository
from database.repositories.category_repository import CategoryRepository
from database.repositories.import_repository import ImportRepository
from database.repositories.merchant_repository import MerchantRepository
from database.repositories.transaction_repository import TransactionRepository


class ImportService:

    def __init__(self, session: Session):
        self.session = session

        self.import_repo = ImportRepository(session)
        self.merchant_repo = MerchantRepository(session)
        self.category_repo = CategoryRepository(session)
        self.account_repo = AccountRepository(session)
        self.transaction_repo = TransactionRepository(session)