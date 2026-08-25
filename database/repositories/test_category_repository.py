# Test 1
# delete category without transactions and budgets

from datetime import date, datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from database.engine import engine
from database.models.merchant import Merchant
from database.models.transaction import Transaction
from database.models.source_file import Import
from database.models.category import Category
from database.models.account import Account
from database.models.enums import TransactionType
from database.models.enums import Currency
from database.models.enums import Colors
from database.models.enums import Status
from database.repositories.category_repository import CategoryRepository

with Session(engine) as session:
    with session.begin():

