import datetime

from sqlalchemy.orm import Session

from database.repositories.account_repository import AccountRepository
from database.repositories.category_repository import CategoryRepository
from database.repositories.import_repository import ImportRepository
from database.repositories.merchant_repository import MerchantRepository
from database.repositories.transaction_repository import TransactionRepository
from database.models.enums import Currency
from models.enums import Status
from src.classification.detect_merchant import normalize_merchant_name
from src.classification.extract_location import extract_location
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

    # Import transactions
    def import_transactions(self, file_path: str):
        # 1. We need to run the data pipeline to prepare data for work
        df, bank = run_pipeline(file_path)
        account_number = df["account_number"].iloc[0]
        date = df["transaction_date"].max().date()

        # 2. Create import
        new_import = self.import_repo.create_source_file(bank=bank, date=date)

        # 3. Create account
        account = self.account_repo.get_by_account_name(account_number)

        if account is None:
            account = self.account_repo.create(
                bank=bank,
                account_name=account_number,
                currency=Currency(df["currency_code"].iloc[0]),
                created_at=datetime.date.today()
            )

        # 4. Create merchants
        # We need to loop through every row to check if merchant exists if not then create a new one
        for _, row in df.iterrows():
            description = row["transaction_description"]
            normalized_name = normalize_merchant_name(description)
            location = extract_location(description)
            merchant = self.merchant_repo.get_by_normalized_name_and_location(normalized_name=normalized_name, location=location)
            if merchant is None:
                merchant = self.merchant_repo.create(name=f"{normalized_name} - {location}", normalized_name=normalized_name, location=location)

        # 5. Find/Create categories
