from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "python or c, in one sentences!"}],
)
print(resp.choices[0].message.content)