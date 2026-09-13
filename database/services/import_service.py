from sqlalchemy.orm import Session

from database.repositories.account_repository import AccountRepository
from database.repositories.category_repository import CategoryRepository
from database.repositories.import_repository import ImportRepository
from database.repositories.merchant_repository import MerchantRepository
from database.repositories.transaction_repository import TransactionRepository
from src.pipeline.identify_bank import identify_bank
from src.pipeline.data_pipeline import run_pipeline


class ImportService:

    def __init__(self, session: Session):
        self.session = session

        self.import_repo = ImportRepository(session)
        self.merchant_repo = MerchantRepository(session)
        self.category_repo = CategoryRepository(session)
        self.account_repo = AccountRepository(session)
        self.transaction_repo = TransactionRepository(session)

    # 1. Import transactions
    def import_transactions(self, file_path: str):
        # 1. We need to run the data pipeline to prepare data for work
        df, bank = run_pipeline('data/raw/transactions.csv')
        # 2. Create import
        new_import = self.import_repo.create_source_file(bank=bank, date="2026-05-09")