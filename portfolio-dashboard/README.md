# Crypto Portfolio Dashboard

A Python script that fetches live prices for multiple cryptocurrencies, calculates total portfolio value, and updates a Google Sheet automatically.

## Features
- Fetches current prices for Bitcoin, Ethereum, and Solana.
- Calculates portfolio value based on your holdings.
- Updates a Google Sheet with coin details and total value.
- Handles API errors gracefully.

## How to Run
1. Install required libraries:
   ```bash
   pip install gspread oauth2client requests
2. Set up Google Sheets API and download your JSON key file.
3. Place the key file in the same folder as the script.

4. Run the script:
   python portfolio_dashboard.py

# Example Output
✅ Google Sheet updated successfully!
Total Portfolio Value: $51,257.95
Bitcoin: 0.5 @ $72,293.00 = $36,146.50
Ethereum: 5 @ $2,121.29 = $10,606.45
Solana: 50 @ $90.10 = $4,505.00

# Screenshots
<img width="977" height="765" alt="portfolio-dashboard" src="https://github.com/user-attachments/assets/fa57ae89-2ddb-4e85-87b3-d7e0c284b7da" />
