import requests
from communities_db import COMMUNITIES

GROQ_API_KEY = "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"

def build_community_list():
    return "\n".join(
        f"{group} | {c['name']} | {c['url']}"
        for group, items in COMMUNITIES.items()
        for c in items
    )


def get_recommendation(user_interest: str):
    prompt = f"""
Подбери студенческие объединения ВятГУ по интересу.

Интерес:
{user_interest}

Список:
{build_community_list()}

Ответь кратко:

🎯 Группа: <название>

1. <название> — <ссылка>
2. <название> — <ссылка>
(максимум 3 варианта)
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    data = response.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "ошибка")
