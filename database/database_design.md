# 1. Entities:
a) Transaction
- id
- currency
- transaction_date
- amount
- merchant_id
- description
- category_id
- account_id
- transaction_type
- source_file_id
- counterparty_account

b) Account
- id
- bank
- account_name
- currency
- created_at

c) Category
- id
- name
- icon
- color

d) Merchant
- id
- name
- normalized_name
- location
- is_active

e) Import
- id
- filename
- bank
- date
- import_status
- created_at
- rows_count

f) Budget
- id
- category_id
- monthly_limit
- start_date
- end_date


------------------------------
# Relacje:
1. ACCOUNT 1:N --- TRANSACTION
Wiele transakcji może mieć to samo konto, ale tylko jedno konto może być w transakcji
2. TRANSACTION N:1 CATEGORY
Transakcja może mieć tylko jedną kategorię, Jedna kategoria może być przypisana do 1 transakcji 
3. TRANSACTION N:1 MERCHANT
Wiele transakcji może być tego samego merchanta, ale jeden merchant może być w jednej transakcji
4. TRANSACTION N:1 Import
wiele transakcji może nalezec do jednego importu
5. BUDGET N:1 CATEGORY
Ta sama kategoria może mieć kilka budżetów, ponieważ start date i end date mogą być inne już

# Reguły biznesowe:
- Nie można usunąć kategorii, jeżeli jest ona przypisana do transakcji, budżetu
- Każda transakcja musi mieć obowiązkowo jedną kategorię
- Nie można ustawić budżetu na liczbę ujemną
- Nie można ustawić start_date budżetu większy niż end_date
- Każdy merchant z tą samą nazwą, ale z inną lokalizacją to jest osobny nowy merchant
- Usunięcie importu nie usuwa transakcji
- Nie można usuwać merchant, najwyżej, jeżeli jakiś merchant przestaje istnieć no to możemy dodać pole ze statusem open czy closed, zeby wiedzieć
- Imię kategorii musi byc unikalne, nie mozemy takich samych tworzyc
- account_name musi byc unikalne, nie moze byc takich samych kont
