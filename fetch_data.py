import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://www.bankofcanada.ca/valet/observations/V80691311/json?start_date=2021-05-11"
response = requests.get(url)
data = response.json()

dates = []
rates = []

for observation in data["observations"]:
    dates.append(observation["d"])
    rates.append(float(observation["V80691311"]["v"]))

df = pd.DataFrame({
    "date": dates,
    "mortgage_rate": rates
})

df.to_csv("mortgage_rates.csv", index=False)
print(f"Saved {len(df)} rows to mortgage_rates.csv")
print(df.head())

plt.figure(figsize=(12, 6))
plt.plot(dates, rates)
plt.title("Canada 5-Year Conventional Mortgage Rate (2021-2026)")
plt.xlabel("Date")
plt.ylabel("Rate (%)")
plt.xticks(dates[::20], rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("mortgage_rates_chart.png")
plt.show()