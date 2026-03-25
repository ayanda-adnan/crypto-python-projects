# Bitcoin Price Tracker

A Python script that fetches the current Bitcoin price from the CoinGecko API and logs it to a CSV file with a timestamp.

## Features
- Fetches live Bitcoin price in USD.
- Saves data to `bitcoin_prices.csv` with timestamp.
- Handles errors gracefully (e.g., no internet).

## How to Run
1. Install required library:
   ```bash
   pip install requests

# Run the script
python price_tracker.py

# Example Output
Bitcoin price: $71234
✓ Saved to bitcoin_prices.csv

# Screenshots
<img width="876" height="679" alt="price_tracker" src="https://github.com/user-attachments/assets/aa65edd3-82bb-48cd-964b-d1772c94563a" />

