import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Canadian Housing Affordability", layout="wide")

df = pd.read_csv("affordability.csv")

st.title("Canadian Housing Affordability Dashboard")
st.markdown(
    "An interactive look at how housing affordability has changed across major "
    "Canadian cities, combining Bank of Canada mortgage rates with Statistics "
    "Canada home price and income data."
)

st.sidebar.header("Filters")
all_cities = sorted(df["GEO"].unique())
selected_cities = st.sidebar.multiselect(
    "Select cities to compare:",
    options=all_cities,
    default=all_cities
)

year_range = st.sidebar.slider(
    "Year range:",
    int(df["YEAR"].min()),
    int(df["YEAR"].max()),
    (int(df["YEAR"].min()), int(df["YEAR"].max()))
)

filtered = df[
    (df["GEO"].isin(selected_cities)) &
    (df["YEAR"] >= year_range[0]) &
    (df["YEAR"] <= year_range[1])
]

col1, col2, col3 = st.columns(3)
latest_year = filtered["YEAR"].max()
latest = filtered[filtered["YEAR"] == latest_year]

if not latest.empty:
    worst_city = latest.loc[latest["affordability_ratio"].idxmax()]
    best_city = latest.loc[latest["affordability_ratio"].idxmin()]
    avg_ratio = latest["affordability_ratio"].mean()

    col1.metric("Least Affordable", worst_city["GEO"].split(",")[0], f"{worst_city['affordability_ratio']:.1f}% of income")
    col2.metric("Most Affordable", best_city["GEO"].split(",")[0], f"{best_city['affordability_ratio']:.1f}% of income")
    col3.metric(f"Avg Across Cities ({latest_year})", f"{avg_ratio:.1f}%", "of household income")

st.subheader("Affordability Ratio Over Time")
fig = px.line(
    filtered,
    x="YEAR",
    y="affordability_ratio",
    color="GEO",
    markers=True,
    labels={"affordability_ratio": "% of Income for Mortgage", "YEAR": "Year", "GEO": "City"}
)
fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="30% affordability threshold")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Underlying Data")
st.dataframe(
    filtered[["GEO", "YEAR", "estimated_home_price", "median_income", "mortgage_rate", "monthly_payment", "affordability_ratio"]]
    .sort_values(["GEO", "YEAR"])
    .round(2),
    use_container_width=True
)

st.markdown("---")
st.markdown(
    "**Methodology:** Estimated home prices are anchored to approximate 2018 new-home "
    "averages and scaled using StatsCan's New Housing Price Index. Monthly mortgage "
    "payments assume 20% down on a 25-year amortization at the year's average 5-year "
    "conventional mortgage rate. Sources: Bank of Canada Valet API, StatsCan tables "
    "18-10-0205 and 11-10-0190."
)