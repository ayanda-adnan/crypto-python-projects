# Import the libraries we need
import requests  # This lets us fetch data from the websites/APIs
import csv   #This helps us save data to CVS files
from datetime import datetime  # This gives us the current date and time for the timestamps
import time  #NEW : This lets us pause the program between checks

# Configuration - you can change these values
THRESHOLD = 70000  # Alerts when bitcoin drops below $70,000
CHECK_INTERVAL = 60 # Checks the price every 60 seconds

def get_bitcoin_price():
    """Fetch current Bitcoin price from CoinGecko"""

    # The API endpoint for bitcoin price in USD
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    
    try:
        # Send request to the API
        response = requests.get(url)
        # Convert request from JSON to Python dictionary
        data = response.json()
        # Extract just the price number 
        price = data['bitcoin']['usd']
        # Send the price to whaever this functon was called 
        return price
    except Exception as e:
        # If anything goes wrong 
        print(f"Error fetching price: {e}")
        # Return none to indicate something went wrong
        return None

def log_alert(price, threshold):
    """Save alert details to a separate CSV file"""

    # Get current times in redable format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open the alerts CVS file
    # 'a' ,eans append, add new data without deleting old data
    with open('bitcoin_alerts.csv', 'a', newline='') as file:
        # Create a CVS writer object
        writer = csv.writer(file)
        # Write one row with timestamp, price that triggered,and threshold
        writer.writerow([timestamp, price, threshold])
    # print confirmation so you know it worked
    print(f"🚨 ALERT LOGGED: ${price} dropped below ${threshold}")

# Print startup message
print(f"Starting Bitcoin monitor. Alert threshold: ${THRESHOLD}")
print("Press Ctrl+C to stop\n")
# Main Loop- runs forever until you stop it
while True:
    # Get current bitcoin price by calling our function
    price = get_bitcoin_price()
    # Only proceed if we got a valid price
    if price is not None:
        # Show current price in terminal
        print(f"Current price: ${price}")
        # Check if price is below threshold
        if price < THRESHOLD:
            # Print alert to terminal
            print(f"🚨 ALERT! Bitcoin dropped below ${THRESHOLD}!")
            # Save alert to CVS by calling our logging function
            log_alert(price, THRESHOLD)
    # P
    time.sleep(CHECK_INTERVAL)