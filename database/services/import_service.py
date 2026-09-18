import datetime
from sqlalchemy.orm import Session

from database.repositories.account_repository import AccountRepository
from database.repositories.category_repository import CategoryRepository
from database.repositories.import_repository import ImportRepository
from database.repositories.merchant_repository import MerchantRepository
from database.repositories.transaction_repository import TransactionRepository
from database.models.enums import Currency
from database.models.enums import Status, CategoryType
from database.models.enums import TransactionType
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
        print("START IMPORT...")
        with self.session.begin():
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
            for index, row in df.iterrows():
                description = row["transaction_description"]
                counterparty_name = row["counterparty_name"]
                normalized_name = normalize_merchant_name(description)
                location = extract_location(description, counterparty_name)
                merchant = self.merchant_repo.get_by_normalized_name_and_location(normalized_name=normalized_name, location=location)
                if merchant is None:
                    merchant = self.merchant_repo.create(name=f"{normalized_name} - {location}", normalized_name=normalized_name, location=location)

                # Assign to every row merchant id it is related to
                df.loc[index, "merchant_id"] = merchant.id

            # 5. Find/Create categories
            # First we need to check if category exists
            for index, row in df.iterrows():
                category_name = row["transaction_category"]
                category = self.category_repo.get_by_name(category_name)
                if category is None:
                    category = CategoryType(category_name)
                    category = self.category_repo.create(name=category_name, icon=category.icon, color=category.color)
                # Assign to every row category id it is related to
                df.loc[index, "category_id"] = category.id


            # 6. Create Transactions
            for _, row in df.iterrows():
                transaction_identifier = row["transaction_identifier"]
                # Check if transaction already created
                transaction = self.transaction_repo.get_by_identifier(transaction_identifier)
                transaction_date = row["transaction_date"]
                currency = row["currency_code"]
                amount = row["debit_amount"] if row["debit_amount"] < 0 else row["credit_amount"]
                transaction_merchant_id = row["merchant_id"]
                transaction_category_id = row["category_id"]
                original_description = row["transaction_original_description"]
                cleaned_description = row["transaction_description"]
                transaction_type = TransactionType(row["transaction_type"].upper())
                counterparty_account = row['counterparty_account']
                # If not then create transaction
                if transaction is None:
                    transaction = self.transaction_repo.create(currency=Currency(currency), transaction_date=transaction_date, amount=amount, merchant_id=transaction_merchant_id, original_description=original_description,
                                          cleaned_description=cleaned_description, category_id=transaction_category_id, account_id=account.id, transaction_type=transaction_type,
                                          source_file_id=new_import.id, counterparty_account=counterparty_account, transaction_identifier=transaction_identifier)
            # 7. Final step update IMPORT status and rows count
            self.import_repo.update(import_id=new_import.id, import_status=Status.SUCCESS, rows_count=len(df))