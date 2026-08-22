from sqlalchemy import select, and_, update
from sqlalchemy.orm import Session
from database.models.merchant import Merchant

# ----------- BUSINESS LOGIC -----------
# 1. Create merchant
# 2. Find by ID
# 3. Find by Normalized Name
# 4. Find Merchants by LOCATION
# 5. Find by Normalized Name and Location
# 6. Update merchant

class MerchantRepository:
    def __init__(self, session: Session):
        self.session = session

    # 1. Create merchant
    def create(self, name: str, normalized_name: str, location: str) -> Merchant:
        merchant = Merchant(name=name, normalized_name=normalized_name, location=location)
        self.session.add(merchant)
        return merchant

    # 2. Find by ID
    def get_by_id(self, merchant_id) -> Merchant | None:
        stmt = select(Merchant).where(Merchant.id == merchant_id)
        found_merchant = self.session.execute(stmt).scalar_one_or_none()
        return found_merchant

    # 3. Find by Normalized Name
    def get_by_normalized_name(self, normalized_name) -> list[Merchant]:
        stmt = select(Merchant).where(Merchant.normalized_name == normalized_name)
        # We can get multiple merchants that pass the condition
        found_merchants = list(self.session.execute(stmt).scalars())
        return found_merchants

    # 4. Find by Location
    def get_by_location(self, location: str) -> list[Merchant]:
        stmt = select(Merchant).where(Merchant.location == location)
        found_merchants = list(self.session.execute(stmt).scalars())
        return found_merchants

    # 5. Find by normalized name and location
    def get_by_normalized_name_and_location(self, normalized_name: str, location: str) -> Merchant | None:
        stmt = select(Merchant).where(and_(Merchant.normalized_name == normalized_name, Merchant.location == location))
        found_merchant = self.session.execute(stmt).scalar_one_or_none()
        return found_merchant

    # 6. Update
    def update(self, merchant_id, name: str | None = None, normalized_name: str | None = None, location: str | None = None) -> Merchant | None:
        stmt = select(Merchant).where(Merchant.id == merchant_id)
        found_merchant = self.session.execute(stmt).scalar_one_or_none()
        # In case there is None result
        if found_merchant is None:
            return None
        # Changing only values that have been passed
        if name is not None:
            found_merchant.name = name
        if normalized_name is not None:
            found_merchant.normalized_name = normalized_name
        if location is not None:
            found_merchant.location = location
        return found_merchant