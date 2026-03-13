# ============================================
# CRYPTO PORTFOLIO DASHBOARD - DAY 3 PROJECT
# ============================================

# --------------------------
# 1. IMPORT THE TOOLS WE NEED
# --------------------------

import gspread
# gspread lets us talk to Google Sheets (read/write)

from oauth2client.service_account import ServiceAccountCredentials
# This handles the login to Google using our secret JSON key file

import requests
# We already know this – it fetches data from the internet (CoinGecko API)

from datetime import datetime
# To add timestamps to our Google Sheet

# --------------------------
# 2. SET UP GOOGLE SHEETS CONNECTION
# --------------------------

# Define what we're allowed to do with Google Sheets
# We need access to sheets themselves and to Google Drive (to find them)
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/drive"]

# Load your service account credentials from the JSON file you downloaded
# Make sure "portfolio-key.json" is in the same folder as this script
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json (2).json", scope)

# Now authorize a client using those credentials
client = gspread.authorize(creds)

# Open your Google Sheet by its name (the title you gave it)
# Replace "Crypto Portfolio" with the actual name of your sheet
sheet = client.open("Crypto Portfolio").sheet1   # sheet1 is the first tab

# --------------------------
# 3. FUNCTION TO FETCH MULTIPLE CRYPTO PRICES
# --------------------------

def get_prices(coin_list):
    """
    Fetches current USD prices for a list of coins from CoinGecko.
    coin_list: a list like ["bitcoin", "ethereum", "solana"]
    Returns a dictionary: {"bitcoin": {"usd": 70000}, "ethereum": {...}}
    """
    # Join the list with commas: ["bitcoin","ethereum"] -> "bitcoin,ethereum"
    coins_string = ",".join(coin_list)
    
    # Build the API URL
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins_string}&vs_currencies=usd"
    
    try:
        # Send the request and get response
        response = requests.get(url)
        # Convert JSON response to Python dictionary
        data = response.json()
        return data
    except Exception as e:
        # If anything goes wrong (no internet, API down), print error and return None
        print(f"❌ Error fetching prices: {e}")
        return None

# --------------------------
# 4. FUNCTION TO CALCULATE PORTFOLIO VALUE
# --------------------------

def calculate_portfolio(prices_dict):
    """
    Uses the price data and your holdings to compute total value.
    prices_dict: the dictionary returned by get_prices()
    Returns: (list_of_rows, total_value)
    """
    # This is where you set how much of each coin you own.
    # Change these numbers to whatever you want.
    holdings = {
        "bitcoin": 0.5,
        "ethereum": 5,
        "solana": 50
    }
    
    total = 0.0
    rows = []   # This will store each coin's data as a row
    
    # Loop through each coin in your holdings
    for coin, amount in holdings.items():
        # prices_dict looks like {"bitcoin": {"usd": 70000}, ...}
        # So we dig in to get the price: prices_dict[coin]["usd"]
        price = prices_dict.get(coin, {}).get("usd", 0)
        # If price is missing, default to 0 (so it doesn't crash)
        
        value = amount * price
        total += value
        
        # Append a row: [coin name, amount, price, value]
        rows.append([coin, amount, price, value])
    
    return rows, total

# --------------------------
# 5. FUNCTION TO UPDATE GOOGLE SHEETS
# --------------------------

def update_sheet(rows, total_value):
    """
    Writes the portfolio data to the Google Sheet.
    rows: list of [coin, amount, price, value]
    total_value: the total portfolio value
    """
    # Optional: clear the sheet before writing new data
    # If you want to keep history, you could append instead.
    sheet.clear()   # This deletes everything! Use carefully.
    
    # Write a header with the current timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([f"Portfolio as of {now}"])
    sheet.append_row([])  # empty row for spacing
    
    # Write column headers
    sheet.append_row(["Coin", "Amount", "Price (USD)", "Value (USD)"])
    
    # Write each coin row
    for row in rows:
        sheet.append_row(row)
    
    # Write a blank row then the total
    sheet.append_row([])
    sheet.append_row(["", "", "TOTAL", total_value])
    
    print("✅ Google Sheet updated successfully!")

# --------------------------
# 6. MAIN PROGRAM – PUT IT ALL TOGETHER
# --------------------------

def main():
    # Step 1: define which coins we want to track
    coins = ["bitcoin", "ethereum", "solana"]
    
    # Step 2: fetch their prices
    prices = get_prices(coins)
    if not prices:
        print("❌ Could not fetch prices. Exiting.")
        return   # stop if prices didn't come through
    
    # Step 3: calculate portfolio value
    rows, total = calculate_portfolio(prices)
    
    # Step 4: update Google Sheet
    update_sheet(rows, total)
    
    # Also print to terminal so you can see it
    print(f"\n💰 Total Portfolio Value: ${total:,.2f}")
    for coin, amount, price, value in rows:
        print(f"{coin.capitalize()}: {amount} @ ${price:,.2f} = ${value:,.2f}")

# This line makes sure main() runs only when you execute the script directly
if __name__ == "__main__":
    main()