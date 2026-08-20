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