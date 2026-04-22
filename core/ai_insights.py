"""
Author: Perfect
Date: 2026-04-17
Description: AI insight helper that summarizes transaction data through the Gemini API.
"""

import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def get_insights(transactions):
    """Generate a short natural-language summary of the provided transaction history."""
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key or api_key == "your_api_key_here":
        raise ValueError("Set your GEMINI_API_KEY in the .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    if not transactions:
        return "No transactions yet. Add some to get insights."

    total_income = sum(t.amount for t in transactions if t.get_type() == "Income")
    total_expense = sum(t.amount for t in transactions if t.get_type() == "Expense")
    balance = total_income - total_expense

    # Group totals by transaction type and category before prompting the model.
    category_totals = {}
    for t in transactions:
        key = f"{t.get_type()} - {t.category}"
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
