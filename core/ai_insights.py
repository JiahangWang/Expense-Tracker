import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def get_insights(transactions):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise ValueError("Set your GEMINI_API_KEY in the .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    if not transactions:
        return "No transactions yet. Add some to get insights."

    total_income  = sum(t.amount for t in transactions if t.get_type() == "Income")
    total_expense = sum(t.amount for t in transactions if t.get_type() == "Expense")
    balance       = total_income - total_expense

    category_totals = {}
    for t in transactions:
        key = f"{t.get_type()} — {t.category}"
        category_totals[key] = category_totals.get(key, 0) + t.amount

    breakdown = "\n".join(f"  {k}: ${v:,.2f}" for k, v in sorted(category_totals.items()))

    prompt = f"""You are a personal finance assistant. Analyze this data and give 3-5 short, practical insights.

Summary:
  Total Income:  ${total_income:,.2f}
  Total Expense: ${total_expense:,.2f}
  Balance:       ${balance:,.2f}

Category Breakdown:
{breakdown}

Be friendly and concise. Use bullet points."""

    return model.generate_content(prompt).text
