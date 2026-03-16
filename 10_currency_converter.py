import requests
import json
from datetime import datetime

API_URL = "https://api.exchangerate-api.com/v4/latest/"

# Fallback rates (relative to USD) — used if API is unavailable
FALLBACK_RATES = {
    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "INR": 83.5, "JPY": 149.5,
    "CAD": 1.36, "AUD": 1.53, "CHF": 0.90, "CNY": 7.24, "MXN": 17.2,
    "BRL": 5.0, "KRW": 1330.0, "SGD": 1.35, "HKD": 7.82, "NOK": 10.6,
    "SEK": 10.5, "DKK": 6.88, "NZD": 1.63, "ZAR": 18.8, "AED": 3.67,
}

CURRENCY_NAMES = {
    "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound",
    "INR": "Indian Rupee", "JPY": "Japanese Yen", "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar", "CHF": "Swiss Franc", "CNY": "Chinese Yuan",
    "MXN": "Mexican Peso", "BRL": "Brazilian Real", "KRW": "South Korean Won",
    "SGD": "Singapore Dollar", "HKD": "Hong Kong Dollar", "AED": "UAE Dirham",
}

history = []


def fetch_rates(base: str) -> dict:
    """Fetch live rates from API. Returns dict of rates."""
    try:
        resp = requests.get(f"{API_URL}{base}", timeout=6)
        resp.raise_for_status()
        data = resp.json()
        return data.get("rates", {}), True
    except Exception:
        # Normalize fallback rates to requested base
        base_rate = FALLBACK_RATES.get(base.upper(), 1.0)
        normalized = {k: round(v / base_rate, 6) for k, v in FALLBACK_RATES.items()}
        return normalized, False


def convert(amount: float, from_cur: str, to_cur: str) -> tuple:
    """Convert amount from one currency to another."""
    from_cur = from_cur.upper()
    to_cur = to_cur.upper()

    rates, live = fetch_rates(from_cur)

    if to_cur not in rates:
        raise ValueError(f"Currency '{to_cur}' not found.")

    result = amount * rates[to_cur]
    return result, live, rates[to_cur]


def display_currency_list():
    """Print common currencies."""
    print("\n  Common Currencies:")
    for code, name in CURRENCY_NAMES.items():
        print(f"  {code:<6} {name}")
    print("  (Many more supported — just enter the 3-letter code)\n")


def main():
    print("=" * 50)
    print("          CURRENCY CONVERTER 💱")
    print("=" * 50)

    while True:
        print("\n  1. Convert currency")
        print("  2. View common currencies")
        print("  3. View conversion history")
        print("  4. Exit")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            try:
                amount_str = input("  Amount: ").strip().replace(",", "")
                amount = float(amount_str)
                if amount < 0:
                    print("  ⚠️  Amount must be positive.")
                    continue
            except ValueError:
                print("  ⚠️  Invalid amount.")
                continue

            from_cur = input("  From currency (e.g. USD): ").strip().upper()
            to_cur   = input("  To currency   (e.g. INR): ").strip().upper()

            if not from_cur or not to_cur:
                print("  ⚠️  Currency codes cannot be empty.")
                continue

            try:
                result, is_live, rate = convert(amount, from_cur, to_cur)
                source = "🌐 Live rate" if is_live else "📦 Offline fallback rate"

                print(f"\n  {amount:,.2f} {from_cur}  =  {result:,.4f} {to_cur}")
                print(f"  1 {from_cur} = {rate:.6f} {to_cur}")
                print(f"  [{source}]")

                entry = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "from": from_cur, "to": to_cur,
                    "amount": amount, "result": result,
                }
                history.append(entry)

            except ValueError as e:
                print(f"  ❌ {e}")

        elif choice == "2":
            display_currency_list()

        elif choice == "3":
            print("\n  📜 Conversion History (last 10):")
            if not history:
                print("  (No conversions yet)")
            else:
                for i, e in enumerate(history[-10:], 1):
                    print(f"  {i:>2}. [{e['time']}]  {e['amount']:>12,.2f} {e['from']}  →  {e['result']:>14,.4f} {e['to']}")

        elif choice == "4":
            print("\n  Goodbye! 💰\n")
            break
        else:
            print("  ⚠️  Invalid choice.")


if __name__ == "__main__":
    main()
