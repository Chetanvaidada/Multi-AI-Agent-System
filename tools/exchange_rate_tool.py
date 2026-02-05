import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://v6.exchangerate-api.com/v6"
@tool
def get_exchange_rate(base: str, target: str):
    """
    Fetch exchange rate from base currency to target currency
    using ExchangeRate-API (latest endpoint).

    Args:
        base (str): Base currency (e.g., USD)
        target (str): Target currency (e.g., INR)

    Returns:
        dict: Exchange rate info or error
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "EXCHANGE_RATE_API_KEY not found. Please set it in your .env file."
        )

    url = f"{BASE_URL}/{api_key}/latest/{base.upper()}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "base": base,
            "target": target,
            "error": str(e)
        }

    data = response.json()

    # API-level error handling
    if data.get("result") != "success":
        return {
            "base": base,
            "target": target,
            "error": data.get("error-type", "Unknown error")
        }

    rates = data.get("conversion_rates", {})
    rate = rates.get(target.upper())

    if rate is None:
        return {
            "base": base.upper(),
            "target": target.upper(),
            "error": "Target currency not found"
        }

    return {
        "base": base.upper(),
        "target": target.upper(),
        "rate": rate,
        "last_updated": data.get("time_last_update_utc")
    }

