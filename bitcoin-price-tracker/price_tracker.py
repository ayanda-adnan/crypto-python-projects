# Import the libraries we need
import requests  #this lets us fetch data from websites/apis
import csv  #this lets us save data to CVS files
from datetime import datetime  # this gives us current time for timestamps

# The URL for CoinGecko's free API to get Bitcoin price in USD
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

try:
    # Send a request to the API and get the response
    response = requests.get(url)
    # Convert the response from JSON format into a python dictionary
    data = response.json()
    
    # Extract the Bitcoin price from the dictionary
    bitcoin_price = data['bitcoin']['usd']
    
    # Print the price so we can see it
    print(f"Bitcoin price: ${bitcoin_price}")
    
    # Save to CSV with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Open (or create) a CVS file to store the data
    with open('bitcoin_prices.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Write one row with the timestamp and price
        writer.writerow([timestamp, bitcoin_price])
    
    print("✓ Saved to bitcoin_prices.csv")
    
except Exception as e:
    print(f"Error: {e}")