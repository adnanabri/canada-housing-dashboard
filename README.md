# Canadian Housing Affordability Dashboard

An interactive dashboard analyzing housing affordability across major Canadian cities, combining real-time Bank of Canada mortgage rate data with Statistics Canada home price and household income data.

## Live Demo

(Coming soon — Streamlit deployment in progress)

## Key Findings

- **Vancouver households now require 67% of pre-tax income** to service a typical mortgage, up from 41% in 2021
- **Toronto crossed the 30% affordability threshold in 2022** and now sits at 46%, driven primarily by rising mortgage rates rather than price growth
- **Calgary doubled its affordability stress in three years** — going from the most affordable major city (16% in 2021) to crossing the 30% threshold in 2023
- Every major Canadian city is now at or above the 30% affordability stress threshold

## Methodology

The dashboard calculates each city's annual mortgage-cost-to-income ratio using:

1. **Estimated home prices** — anchored to approximate 2018 new-home averages and scaled annually using Statistics Canada's New Housing Price Index (Table 18-10-0205)
2. **Median household income** — from Statistics Canada's income table for economic families (Table 11-10-0190)
3. **Mortgage rates** — annualized average of Bank of Canada's 5-year conventional mortgage rate, retrieved via the Valet API
4. **Monthly mortgage payments** — calculated assuming 20% down payment on a 25-year amortization

## Tech Stack

- **Python** — pandas for data processing
- **Streamlit** — interactive dashboard framework
- **Plotly** — interactive visualizations
- **matplotlib** — static charts
- **requests** — Bank of Canada API integration


## Data Pipeline

All three data sources are pulled programmatically — Bank of Canada via Valet REST API, and StatsCan via the Web Data Service API. Re-running `fetch_data.py` and `fetch_statscan.py` refreshes the entire pipeline.

## Project Structure
## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Sources

- [Bank of Canada Valet API](https://www.bankofcanada.ca/valet/docs)
- [StatsCan Table 18-10-0205](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810020501) — New Housing Price Index
- [StatsCan Table 11-10-0190](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110019001) — Income of individuals

## Author

**Adnan Abri** — Economics, Simon Fraser University