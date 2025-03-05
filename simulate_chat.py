import os
import json
from datetime import datetime

import roles


# model_name = "gpt-3.5-turbo"
model_name = "gpt-4"


def load_system_prompt(file_path):
    with open(file_path, 'r') as f:
        system_prompt_dict = json.load(f)
    return system_prompt_dict["system prompt"]


def simulate_one_round():
    chatbot_system_prompt_path = 'system_prompts/chatbot/20240311021613/1.json'
    # older_adult_system_prompt_path = 'system_prompts/older_adult/20240311020321/1.json'
    older_adult_system_prompt_path = 'system_prompts/older_adult_hc/20240311212503/1.json'

    chatbot_system_prompt = load_system_prompt(chatbot_system_prompt_path)
    older_adult_system_prompt = load_system_prompt(older_adult_system_prompt_path)

    chatbot = roles.Chatbot(chatbot_system_prompt, model_name)
    older_adult = roles.Chatbot(older_adult_system_prompt, model_name)

    curr_prompt = "Start with \"Hi, I am Alexa. Nice to meet you virtually.\""

    chat_history_list = []

    for i in range(3):
        curr_chat = dict()
        print("Turn {}:".format(i + 1))

        curr_prompt = chatbot.chat(curr_prompt)
        print("Chatbot: {}".format(curr_prompt))
        curr_chat['chatbot'] = curr_prompt

        curr_prompt = older_adult.chat(curr_prompt)
        print("Older adult: {}".format(curr_prompt))
        curr_chat['older_adult'] = curr_prompt
        chat_history_list.append(curr_chat)

    curr_prompt = chatbot.chat(curr_prompt)
    curr_chat = dict()
    curr_chat['chatbot'] = curr_prompt
    chat_history_list.append(curr_chat)

    inference_prompt = """Now answer if the older adults have Alzheimer's dementia. Think step by step. And finally, output in the JSON format ["Alzheimer's dementia"] with ["true", "false"]. If the result is "possible", please output "true"."""
    inference_result = chatbot.chat(inference_prompt)
    chat_history_list.append({'inference': inference_result})

    save_dir = 'chat_history'
    save_dir = os.path.join(save_dir, datetime.now().strftime('%Y%m%d%H%M%S'))
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, '1.json'), 'w') as f:
        json.dump(chat_history_list, f)


def main():
    simulate_one_round()


if __name__ == '__main__':
    main()
