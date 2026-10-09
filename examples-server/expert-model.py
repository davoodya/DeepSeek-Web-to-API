from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

resp = client.chat.completions.create(
    model="deepseek-expert",
    messages=[{"role": "user", "content": "What changed in the news today?"}],
    extra_body={"thinking": True, "search": True},
)

print(resp.choices[0].message.content)