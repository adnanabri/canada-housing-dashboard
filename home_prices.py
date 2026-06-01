import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/home_prices.csv")

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
    (df["New housing price indexes"] == "Total (house and land)") &
    (df["REF_DATE"] >= "2021-01")
]

print(f"Filtered down to {len(filtered)} rows")
print(filtered[["REF_DATE", "GEO", "VALUE"]].head(10))

plt.figure(figsize=(12, 6))
for city in cities:
    city_data = filtered[filtered["GEO"] == city]
    plt.plot(city_data["REF_DATE"], city_data["VALUE"], label=city)

plt.title("New Housing Price Index by City (2021–2026)")
plt.xlabel("Date")
plt.ylabel("Price Index (2016=100)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("home_prices_chart.png")
plt.show()