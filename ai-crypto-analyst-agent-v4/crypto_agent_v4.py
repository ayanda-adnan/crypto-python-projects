# =============================================
# DAY 4: AI CRYPTO AGENT WITH OUTPUT PARSING
# Structured response using Pydantic
# =============================================

import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pydantic import BaseModel, Field   # For defining data schema
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser   # To parse LLM output into our schema

load_dotenv()

# ----------------------------------------------------------------------
# 1. DEFINE THE STRUCTURED OUTPUT FORMAT
# ----------------------------------------------------------------------
# We tell the AI exactly what data we want. This model will be used by the parser.
class CryptoAnalysis(BaseModel):
    short_term_trend: str = Field(description="24h trend: up/down/sideways")
    medium_term_trend: str = Field(description="7d trend: up/down/sideways")
    risk_assessment: str = Field(description="One sentence describing the biggest risk currently")

# Create a parser that knows how to turn the AI's response into a CryptoAnalysis object.
parser = PydanticOutputParser(pydantic_object=CryptoAnalysis)

# ----------------------------------------------------------------------
# 2. FUNCTIONS TO FETCH DATA (same as v3)
# ----------------------------------------------------------------------
def get_current_price_and_change(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url)
        data = response.json()
        price = data[coin_id]['usd']
        change_24h = data[coin_id]['usd_24h_change']
        return price, change_24h
    except Exception as e:
        print(f"Error fetching current data: {e}")
        return None, None

def get_price_7_days_ago(coin_id):
    date_7_days_ago = (datetime.now() - timedelta(days=7)).strftime("%d-%m-%Y")
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date_7_days_ago}&localization=false"
    try:
        response = requests.get(url)
        data = response.json()
        price = data['market_data']['current_price']['usd']
        return price
    except Exception as e:
        print(f"Error fetching 7-day price: {e}")
        return None

# ----------------------------------------------------------------------
# 3. SETUP LLM AND PROMPT WITH FORMAT INSTRUCTIONS
# ----------------------------------------------------------------------
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# The prompt now includes format instructions from the parser.
# The parser tells the AI what fields to fill and in what format.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a crypto analyst. Given the coin and its price metrics, provide an analysis.\n"
               "{format_instructions}"),
    ("user", "Coin: {coin}\nCurrent price: ${price:.2f}\n24h change: {change_24h:.2f}%\n7‑day change: {change_7d:.2f}%")
])

# We can't use the pipe operator directly because we need to inject format_instructions.
# So we'll create a chain manually: first format the prompt with input, then call the LLM, then parse.
# Alternatively, we can use a RunnableSequence, but for clarity we'll do steps.

# ----------------------------------------------------------------------
# 4. MAIN LOOP
# ----------------------------------------------------------------------
while True:
    coin = input("\nEnter coin ID (e.g., bitcoin, ethereum) or 'quit': ").strip().lower()
    if coin == 'quit':
        break

    # Fetch data
    price, change_24h = get_current_price_and_change(coin)
    if price is None:
        print("Coin not found or API error.")
        continue

    price_7d = get_price_7_days_ago(coin)
    if price_7d is None:
        print("Could not fetch 7‑day price. Skipping analysis.")
        continue

    change_7d = ((price - price_7d) / price_7d) * 100

    print(f"Price: ${price:.2f} | 24h change: {change_24h:.2f}% | 7d change: {change_7d:.2f}%")

    # ------------------------------------------------------------------
    # 5. RUN THE CHAIN WITH OUTPUT PARSING
    # ------------------------------------------------------------------
    # First, get the format instructions from the parser (a string)
    format_instructions = parser.get_format_instructions()

    # Format the prompt with the actual input values
    formatted_messages = prompt.format_messages(
        coin=coin,
        price=price,
        change_24h=change_24h,
        change_7d=change_7d,
        format_instructions=format_instructions
    )

    # Invoke the LLM with the formatted messages
    response = llm.invoke(formatted_messages)

    # Now parse the response into our CryptoAnalysis object
    try:
        parsed = parser.parse(response.content)
        print("\n--- Structured Analysis ---")
        print(f"Short-term trend: {parsed.short_term_trend}")
        print(f"Medium-term trend: {parsed.medium_term_trend}")
        print(f"Risk assessment: {parsed.risk_assessment}")
    except Exception as e:
        # If parsing fails, print the raw response and the error
        print("\n--- Raw Response (Parsing Failed) ---")
        print(response.content)
        print(f"Parsing error: {e}")

    print("-" * 40)