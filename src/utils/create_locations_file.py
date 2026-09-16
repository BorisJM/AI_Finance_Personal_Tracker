from pathlib import Path
import pandas as pd
import json

# AI_Finance_Personal_Tracker/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "SIMC_Urzedowy.csv"
OUTPUT_FILE = BASE_DIR / "data" / "locations.json"

print("Szukam pliku:", INPUT_FILE)
print("Istnieje:", INPUT_FILE.exists())

df = pd.read_csv(
    INPUT_FILE,
    sep=";",
    encoding="utf-8",
    dtype=str
)

print("Kolumny:", df.columns.tolist())

locations = (
    df["NAZWA"]
    .dropna()
    .str.strip()
    .str.upper()
    .drop_duplicates()
    .sort_values()
    .tolist()
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        locations,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"\nGotowe!")
print(f"Liczba miejscowości: {len(locations)}")
print(f"Plik zapisany tutaj: {OUTPUT_FILE}")