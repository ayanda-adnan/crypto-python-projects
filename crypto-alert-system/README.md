# Crypto Alert System

A Python script that continuously monitors the Bitcoin price and sends an alert when it drops below a specified threshold.

## Features
- Fetches live Bitcoin price every 60 seconds.
- Compares price against a user-defined threshold.
- Prints an alert message to the terminal when triggered.
- Logs all alerts to a separate CSV file (`bitcoin_alerts.csv`).

## How to Run
1. Install required library:
   ```bash
   pip install requests

# Run the script
python alert_system.py

# Example Output
Starting Bitcoin monitor. Alert threshold: $70000
Current price: $71234
Current price: $69876
🚨 ALERT! Bitcoin dropped below $70000!
🚨 ALERT LOGGED: $69876 dropped below $70000

# Screenshots
