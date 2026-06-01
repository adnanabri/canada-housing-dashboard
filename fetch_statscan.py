import requests
import zipfile
import io
import pandas as pd
import os


def fetch_statscan_table(product_id, output_path=None):
    """
    Download a StatsCan table via the Web Data Service API.

    Args:
        product_id: The 8-digit product ID (e.g., "18100205" for housing prices)
        output_path: Optional path to save the CSV locally

    Returns:
        A pandas DataFrame with the table data
    """
    api_url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{product_id}/en"
    print(f"Requesting download link for table {product_id}...")
    response = requests.get(api_url)
    response_json = response.json()

    if response_json["status"] != "SUCCESS":
        raise Exception(f"StatsCan API error: {response_json}")

    download_url = response_json["object"]
    print(f"  Got URL: {download_url}")

    print(f"  Downloading ZIP...")
    zip_response = requests.get(download_url)

    zip_file = zipfile.ZipFile(io.BytesIO(zip_response.content))
    csv_filename = [
        name for name in zip_file.namelist()
        if name.endswith(".csv") and "MetaData" not in name
    ][0]
    print(f"  Extracting {csv_filename}...")

    with zip_file.open(csv_filename) as csv_file:
        df = pd.read_csv(csv_file)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"  Saved to {output_path}")

    print(f"  Loaded {len(df)} rows.")
    return df


if __name__ == "__main__":
    print("=" * 60)
    print("Fetching home prices (Table 18-10-0205)...")
    print("=" * 60)
    home_prices = fetch_statscan_table("18100205", "data/home_prices.csv")

    print()
    print("=" * 60)
    print("Fetching income data (Table 11-10-0190)...")
    print("=" * 60)
    income = fetch_statscan_table("11100190", "data/income.csv")

    print()
    print("Done! Both datasets refreshed from StatsCan API.")