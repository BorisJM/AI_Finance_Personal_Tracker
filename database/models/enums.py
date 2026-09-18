from enum import Enum

# Currency ENUM class with options
class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"

class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Colors(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

class Status(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    PENDING = 'PENDING'

# Category type class with icons and colors for each category
class CategoryType(Enum):
    GROCERIES = "Groceries"
    TRAVEL = "Travel"
    PERSONALCARE = "Personal Care"
    TRANSPORT = "Transport"
    HYGIENE = "Hygiene"
    SHOPPING = "Shopping"
    CLOTHES = "Clothes"
    HEALTH_FITNESS = "Health & Fitness"
    CAR = "Car"
    SUBSCRIPTIONS = "Subscriptions"
    FOOD = "Food"
    ALCOHOL = "Alcohol"
    EDUCATION = "Education"
    INCOME = "Income"
    INSURANCE = "Insurance"
    ENTERTAINMENT = "Entertainment"
    TRANSFERS = "Transfers"
    FINANCIAL = "Financial"
    PET = "Pet"
    BILLS_UTILITIES = "Bills & Utilities"
    GIFTS = "Gifts"

    # Category icons
    @property
    def icon(self) -> str:
        CATEGORY_ICONS = {
            CategoryType.GROCERIES: "🛒",
            CategoryType.TRAVEL: "✈️",
            CategoryType.PERSONALCARE: "💈",
            CategoryType.TRANSPORT: "🚕",
            CategoryType.HYGIENE: "🧴",
            CategoryType.SHOPPING: "🛍️",
            CategoryType.CLOTHES: "👕",
            CategoryType.HEALTH_FITNESS: "🏋️",
            CategoryType.CAR: "🚗",
            CategoryType.SUBSCRIPTIONS: "🔄",
            CategoryType.FOOD: "🍔",
            CategoryType.ALCOHOL: "🍺",
            CategoryType.EDUCATION: "🎓",
            CategoryType.INCOME: "💰",
            CategoryType.INSURANCE: "🛡️",
            CategoryType.ENTERTAINMENT: "🎮",
            CategoryType.TRANSFERS: "↔️",
            CategoryType.FINANCIAL: "📈",
            CategoryType.PET: "🐾",
            CategoryType.BILLS_UTILITIES: "🧾",
            CategoryType.GIFTS: "🎁",
        }
        return CATEGORY_ICONS[self]
    # Category colors
    @property
    def color(self) -> str:
        CATEGORY_COLORS = {
            CategoryType.GROCERIES: "#4CAF50",
            CategoryType.TRAVEL: "#2196F3",
            CategoryType.PERSONALCARE: "#E91E63",
            CategoryType.TRANSPORT: "#9C27B0",
            CategoryType.HYGIENE: "#00BCD4",
            CategoryType.SHOPPING: "#FF9800",
            CategoryType.CLOTHES: "#795548",
            CategoryType.HEALTH_FITNESS: "#F44336",
            CategoryType.CAR: "#607D8B",
            CategoryType.SUBSCRIPTIONS: "#673AB7",
            CategoryType.FOOD: "#FF5722",
            CategoryType.ALCOHOL: "#8E24AA",
            CategoryType.EDUCATION: "#3F51B5",
            CategoryType.INCOME: "#00A86B",
            CategoryType.INSURANCE: "#009688",
            CategoryType.ENTERTAINMENT: "#FFC107",
            CategoryType.TRANSFERS: "#78909C",
            CategoryType.FINANCIAL: "#1565C0",
            CategoryType.PET: "#8BC34A",
            CategoryType.BILLS_UTILITIES: "#546E7A",
            CategoryType.GIFTS: "#EC407A",
        }
        return CATEGORY_COLORS[self]