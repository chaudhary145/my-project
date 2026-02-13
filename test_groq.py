from groq import Groq

# ⚠️ Paste your NEW regenerated key here
client = Groq(api_key="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")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",  # We will test this model
    messages=[
        {"role": "user", "content": "Say hello"}
    ]
)

print(response.choices[0].message.content)
