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
            # -------------- MERCHANTS --------------
            # 4. Create merchants
            # Unique merchants set
            unique_merchants = set()
            unique_categories = set()
            unique_transaction_identifiers = {}
            new_transactions_identifiers = set()
            # We need to loop through every row to check if merchant exists if not then create a new one
            for _, row in df.iterrows():
                category_name = row["transaction_category"]
                # Check if transaction already created
                transaction_identifier = row["transaction_identifier"]
                unique_transaction_identifiers[transaction_identifier] = {"row": row, "category_name": category_name}
            existing_transactions_db = self.transaction_repo.get_by_identifiers(
                    transaction_identifiers=unique_transaction_identifiers.keys())
            transactions_dict = {}
            for transaction_db in existing_transactions_db:
                transactions_dict[transaction_db.transaction_identifier] = transaction_db
            for transaction_identifier in unique_transaction_identifiers.keys():
                if transactions_dict.get(transaction_identifier) is None:
                    description = unique_transaction_identifiers[transaction_identifier]["row"]["transaction_description"]
                    counterparty_name = unique_transaction_identifiers[transaction_identifier]["row"]["counterparty_name"]
                    normalized_name = normalize_merchant_name(description)
                    location = extract_location(description, counterparty_name)
                    unique_merchant = (normalized_name, location)
                    unique_merchants.add(unique_merchant)
                    unique_categories.add(unique_transaction_identifiers[transaction_identifier]["category_name"])
                    unique_transaction_identifiers[transaction_identifier]["location"] = location
                    unique_transaction_identifiers[transaction_identifier]["normalized_name"] = normalized_name
                    new_transactions_identifiers.add(transaction_identifier)
            # If no new transactions to import
            if not new_transactions_identifiers:
                self.import_repo.update(import_id=new_import.id, import_status=Status.SUCCESS, rows_count=len(df))
                return

            existing_merchants_db = self.merchant_repo.get_by_keys(unique_merchants=unique_merchants)
            merchants_dict = {}
            for merchant_db in existing_merchants_db:
                merchants_dict[(merchant_db.normalized_name, merchant_db.location)] = merchant_db
            # Check unique merchants, if merchants_dict doesn't have merchant then we create it and add to the dictionary
            for unique_merchant in unique_merchants:
                normalized_name = unique_merchant[0]
                location = unique_merchant[1]
                if merchants_dict.get((normalized_name, location)) is None:
                    new_merchant = self.merchant_repo.create(name=f"{normalized_name} - {location}",
                                                         normalized_name=normalized_name, location=location)
                    merchants_dict[(normalized_name, location)] = new_merchant
            # -------------- CATEGORIES --------------
            # 5. Find/Create categories
            # First we need to check if category exists
            # Get all categories that are created in database already
            existing_categories_db = self.category_repo.get_by_names(unique_categories=unique_categories)
            categories_dict = {}
            for category_db in existing_categories_db:
                categories_dict[category_db.name] = category_db
            for category_name in unique_categories:
                if categories_dict.get(category_name) is None:
                    new_category = CategoryType(category_name)
                    new_category = self.category_repo.create(name=category_name, icon=new_category.icon, color=new_category.color)
                    categories_dict[category_name] = new_category
            self.session.flush()
            for transaction_identifier in new_transactions_identifiers:
                row = unique_transaction_identifiers[transaction_identifier]["row"]
                transaction_date = row["transaction_date"]
                currency = row["currency_code"]
                amount = row["debit_amount"] if row["debit_amount"] < 0 else row["credit_amount"]
                original_description = row["transaction_original_description"]
                cleaned_description = row["transaction_description"]
                normalized_name = unique_transaction_identifiers[transaction_identifier]["normalized_name"]
                location = unique_transaction_identifiers[transaction_identifier]["location"]
                merchant = merchants_dict.get((normalized_name, location))
                transaction_type = TransactionType("INCOME" if row["credit_amount"] > 0 else "EXPENSE")
                category = categories_dict.get(row["transaction_category"])
                counterparty_account = row['counterparty_account']
                # Check if merchant_id exists
                if merchant is None:
                    raise ValueError(f"Merchant is None for transaction: {transaction_identifier}")
                # Check if category_id exists
                if category is None:
                    raise ValueError(f"Category is None for transaction: {transaction_identifier}")
                transaction_merchant_id = merchant.id
                transaction_category_id = category.id
                transaction = self.transaction_repo.create(currency=Currency(currency),
                                                           transaction_date=transaction_date, amount=amount,
                                                           merchant_id=transaction_merchant_id,
                                                           original_description=original_description,
                                                           cleaned_description=cleaned_description,
                                                           category_id=transaction_category_id,
                                                           account_id=account.id, transaction_type=transaction_type,
                                                           source_file_id=new_import.id,
                                                           counterparty_account=counterparty_account,
                                                           transaction_identifier=transaction_identifier)
            # 7. Final step update IMPORT status and rows count
            self.import_repo.update(import_id=new_import.id, import_status=Status.SUCCESS, rows_count=len(df))


