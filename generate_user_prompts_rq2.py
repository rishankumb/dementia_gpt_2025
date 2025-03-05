import os

import models

system_prompts_dir = 'meta_prompts'
output_dir = 'user/healthy'

# model_name = "gpt-3.5-turbo"
# model_name = "gpt-4"
# model = models.OpenAIModel(model_name)

model_name = 'meta-llama/Meta-Llama-3-8B-Instruct'
model = models.LLM(model_name)


def generate_prompt(template):
    return template


def get_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = model.query_model(messages)
    return response.strip()


def generate_chatbot_prompts(chatbot_key):
    template_path = os.path.join(system_prompts_dir, f'user_generator.txt')

    with open(template_path, 'r') as file:
        template = file.read()

    users = []

    for i in range(50):
        prompt = generate_prompt(template)
        response = get_response(prompt)
        users.append((i + 1, response))
        print(f"Prompt:\n{prompt}\n\nResponse:\n{response}\n{'-' * 50}\n")

    return users


def save_user(user_id, user, output_dir):
    filepath = os.path.join(output_dir, f'user_{user_id}.txt')
    with open(filepath, 'w') as f:
        f.write(user)


def main():
    chatbot_key = 'chatbot'
    users = generate_chatbot_prompts(chatbot_key)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for user_id, user in users:
        save_user(user_id, user, output_dir)


if __name__ == '__main__':
    main()
