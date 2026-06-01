import pandas as pd
import matplotlib.pyplot as plt

home_prices = pd.read_csv("data/home_prices.csv")
income = pd.read_csv("data/income.csv")
mortgage = pd.read_csv("mortgage_rates.csv")

cities = [
    "Toronto, Ontario",
    "Vancouver, British Columbia",
    "Calgary, Alberta",
    "Montréal, Quebec",
]

baseline_prices_2018 = {
    "Toronto, Ontario": 850000,
    "Vancouver, British Columbia": 1150000,
    "Calgary, Alberta": 510000,
    "Montréal, Quebec": 420000,
}

hp = home_prices[
    (home_prices["GEO"].isin(cities)) &
    (home_prices["New housing price indexes"] == "Total (house and land)")
].copy()
hp["YEAR"] = hp["REF_DATE"].str[:4].astype(int)
hp_annual = hp.groupby(["GEO", "YEAR"])["VALUE"].mean().reset_index()
hp_annual.rename(columns={"VALUE": "price_index"}, inplace=True)

inc = income[
    (income["GEO"].isin(cities)) &
    (income["Income concept"] == "Median total income") &
    (income["Economic family type"] == "Economic families")
].copy()
inc.rename(columns={"REF_DATE": "YEAR", "VALUE": "median_income"}, inplace=True)
inc = inc[["GEO", "YEAR", "median_income"]]

mortgage["YEAR"] = mortgage["date"].str[:4].astype(int)
mort_annual = mortgage.groupby("YEAR")["mortgage_rate"].mean().reset_index()

df = hp_annual.merge(inc, on=["GEO", "YEAR"]).merge(mort_annual, on="YEAR")

baseline_index_2018 = hp_annual[hp_annual["YEAR"] == 2018].set_index("GEO")["price_index"]
df["baseline_price"] = df["GEO"].map(baseline_prices_2018)
df["index_2018"] = df["GEO"].map(baseline_index_2018)
df["estimated_home_price"] = df["baseline_price"] * df["price_index"] / df["index_2018"]

df["loan_amount"] = df["estimated_home_price"] * 0.80
df["monthly_rate"] = df["mortgage_rate"] / 100 / 12
df["n_payments"] = 25 * 12
df["monthly_payment"] = df["loan_amount"] * (
    df["monthly_rate"] * (1 + df["monthly_rate"]) ** df["n_payments"]
) / ((1 + df["monthly_rate"]) ** df["n_payments"] - 1)

df["affordability_ratio"] = (df["monthly_payment"] * 12) / df["median_income"] * 100
df.to_csv("affordability.csv", index=False)

print("Housing Affordability by City and Year:")
print(df[["GEO", "YEAR", "estimated_home_price", "median_income", "mortgage_rate", "monthly_payment", "affordability_ratio"]].sort_values(["GEO", "YEAR"]).to_string(index=False))

plt.figure(figsize=(12, 6))
for city in cities:
    city_data = df[df["GEO"] == city].sort_values("YEAR")
    plt.plot(city_data["YEAR"], city_data["affordability_ratio"], marker="o", linewidth=2, label=city)

plt.axhline(y=30, color="red", linestyle="--", alpha=0.6, label="30% affordability threshold")
plt.title("Housing Affordability by City\n(Annual Mortgage Cost as % of Median Household Income)")
plt.xlabel("Year")
plt.ylabel("% of Income Required for Mortgage")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("affordability_chart.png")
plt.show()