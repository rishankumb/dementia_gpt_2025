import os
from datetime import datetime

import models

system_prompts_dir = 'system_prompts'

# model_name = "gpt-3.5-turbo"
model_name = "gpt-4"
model = models.OpenAIModel(model_name)

# model_name = 'meta-llama/Meta-Llama-3-8B-Instruct'
# model = models.LLM(model_name)


def generate_chatbot_prompts(chatbot_key, num=1):
    with open('meta_prompts/{}.txt'.format(chatbot_key), 'r') as f:
        meta_prompt = f.read()
    chatbot_prompt_list = []

    save_dir = os.path.join(system_prompts_dir, chatbot_key, datetime.now().strftime('%Y%m%d%H%M%S'))
    os.makedirs(save_dir, exist_ok=True)

    for i in range(num):
        chatbot_prompt = model.inference(meta_prompt)
        chatbot_prompt_list.append(chatbot_prompt)
        with open(os.path.join(save_dir, '{}.json'.format(i + 1)), 'w') as f:
            f.write(chatbot_prompt)

    return chatbot_prompt_list


def main():
    chatbot_key = 'chatbot'
    # chatbot_key = 'older_adult_ad'
    # chatbot_key = 'older_adult_hc'
    generate_chatbot_prompts(chatbot_key)


if __name__ == '__main__':
    main()
