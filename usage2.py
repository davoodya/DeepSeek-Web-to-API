from deepseek import DeepSeekClient

client = DeepSeekClient()                # loads your signed-in session
replay_num = 0

print(f"replay {replay_num}\n")
# Get a full reply
reply = client.chat("Hi there, Write Python code for generate bubble algorithm")
print(reply.text)

replay_num += 1
print(f"replay {replay_num}\n")

# Continue the SAME conversation — pass the id back
reply2 = client.chat("now write another code with same language for sort algorithm", conversation_id=reply.conversation_id)
print(reply2.text)

replay_num += 1
print(f"replay {replay_num}\n")

# Stream the answer as it's typed
for chunk in client.stream("describe 'Stream the answer as it's typed' in DeepSeek Client, like: for chunk in client.stream print(chunk, end="", flush=True)"):
    print(chunk, end="", flush=True)