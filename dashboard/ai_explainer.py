# ai_explainer.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_explanation(drivers, risk_score):

    # fallback if no key
    if not os.getenv("OPENAI_API_KEY"):
        return "AI explanation unavailable (no API key set)."

    prompt = f"""
You are a pharmaceutical supply chain analyst.

Explain why a drug is at risk of shortage in clear, business-friendly language.

Risk Score: {round(risk_score, 2)}
Key Drivers: {", ".join([d[0] for d in drivers])}

Keep it concise (2–3 sentences).
Focus on actionable insight.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # fast + cheap
            messages=[
                {"role": "system", "content": "You explain supply chain risk clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "AI explanation unavailable. Check rule-based explanation."