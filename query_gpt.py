from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
next_turn = {"role": completion.choices[0].message.role, "content": completion.choices[0].message.content}
print(next_turn)
print(completion.choices[0].finish_reason)
print(completion.usage)
print()
