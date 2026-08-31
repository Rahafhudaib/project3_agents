from openai import OpenAI
import config

_client = None


def get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


def chat(messages, temperature=0.2):
    client = get_client()
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content
