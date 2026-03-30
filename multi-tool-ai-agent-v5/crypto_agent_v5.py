import requests
import feedparser
from talipp.indicators import RSI
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# ---------- TOOLS ----------
def get_price(coin: str) -> str:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        data = requests.get(url).json()
        return f"${data[coin]['usd']:.2f}"
    except:
        return "unavailable"

def get_news() -> str:
    feed = feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/")
    headlines = [entry.title for entry in feed.entries[:3]]
    return "\n".join(headlines) if headlines else "No news found."

def get_rsi(coin: str) -> str:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=100&interval=daily"
    try:
        data = requests.get(url).json()
        prices = [p[1] for p in data['prices']]
        rsi = RSI(14)
        for p in prices:
            rsi.add(p)
        return f"{rsi[-1]:.2f}"
    except:
        return "unavailable"

# ---------- MAIN LOOP ----------
print("Crypto Investment Advisor ready. Ask naturally, e.g., 'Should I buy Bitcoin?'")
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ['quit', 'exit']:
        break

    # Simple keyword detection to fetch data
    coin = None
    if "bitcoin" in user_input.lower() or "btc" in user_input.lower():
        coin = "bitcoin"
    elif "ethereum" in user_input.lower() or "eth" in user_input.lower():
        coin = "ethereum"
    elif "solana" in user_input.lower() or "sol" in user_input.lower():
        coin = "solana"

    context = []
    if coin:
        context.append(f"Current price of {coin}: {get_price(coin)}")
        context.append(f"14-day RSI of {coin}: {get_rsi(coin)}")
    # Always add news for investment questions
    if "buy" in user_input.lower() or "invest" in user_input.lower() or "should" in user_input.lower():
        context.append(f"Recent crypto news:\n{get_news()}")

    context_str = "\n".join(context) if context else "No specific data fetched."

    # Final prompt with real data
    final_prompt = f"""You are a crypto investment advisor. Use the data below to answer the user's question. Be concise, practical, and mention risks. Do not give absolute financial advice – frame as analysis.

User question: {user_input}
Data:
{context_str}

Answer:"""
    response = llm.invoke(final_prompt)
    print(f"\nAdvisor: {response.content}")