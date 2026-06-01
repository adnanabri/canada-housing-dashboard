import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/income.csv")

cities = [
    "Toronto, Ontario",
    "Vancouver, British Columbia",
    "Calgary, Alberta",
    "Montréal, Quebec",
    "Ottawa-Gatineau, Ontario part, Ontario/Quebec",
    "Halifax, Nova Scotia"
]

filtered = df[
    (df["GEO"].isin(cities)) &
    (df["Income concept"] == "Median total income") &
    (df["Economic family type"] == "Economic families") &
    (df["REF_DATE"] >= 2018)
]

print(f"Filtered down to {len(filtered)} rows")
print()
print("Income by city and year:")
print(filtered[["REF_DATE", "GEO", "VALUE"]].sort_values(["GEO", "REF_DATE"]))

plt.figure(figsize=(12, 6))
for city in cities:
    city_data = filtered[filtered["GEO"] == city].sort_values("REF_DATE")
    plt.plot(city_data["REF_DATE"], city_data["VALUE"], marker="o", label=city)

plt.title("Median Household Income by City (Economic Families)")
plt.xlabel("Year")
plt.ylabel("Median Income (CAD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("income_chart.png")
plt.show()