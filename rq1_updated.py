import os
import json

import re
import models

# model_name = 'meta-llama/Meta-Llama-3-8B-Instruct'
model_name = 'gpt-3.5-turbo'
model = models.OpenAIModel(model_name)

file_path = 'rq1_prompts/topics.txt'

found_pattern = "1. Difficulty finding the right words 2. Repetition 3. Substitution of words"


def load_prompt_dict():
    prompt_dir = "rq1_prompts"
    prompt_type = "probing_prompts"
    contexts_json_path = os.path.join(prompt_dir, prompt_type + '.json')
    with open(contexts_json_path, 'r', encoding='utf-8') as f:
        prompt_dict = json.load(f)
    return prompt_dict


def main():
    pattern = r'\d+\.\s*(.*?)'
    pattern_matches = re.findall(pattern, found_pattern)
    print(pattern_matches)
    # pattern_response, pattern_messages = list_pattern()
    # pattern = re.compile(r"\*\*(.*?)\*\*")
    # pattern_matches = pattern.findall(pattern_response)
    # extracted_pattern = []
    # for i, match in enumerate(pattern_matches):
    #     extracted_pattern.append(match)

    # topic_response = list_topics()
    # print("Line 31")
    # print(topic_response)

    # topic = "childhood memory"
    # dialogue_response, dialogue_messages = generate_dialogue(pattern_messages.copy(), topic)
    # print(dialogue_response)
    #
    # find_pattern_response = find_patterns(dialogue_response)
    # print(find_pattern_response)


# def list_pattern(context=''):
#     list_patterns_prompt = load_prompt_dict()['list_patterns']
#     if context:
#         list_patterns_prompt = context + "\n\n" + list_patterns_prompt
#     messages = [{"role": "user", "content": str(list_patterns_prompt)}]
#     response = model.inference_with_messages(messages)
#     messages.append({"role": "assistant", "content": response})
#     return response, messages


# def list_topics():
#     try:
#         with open(file_path, 'r') as file:
#             content = file.readlines()
#         topics = []
#         for line in content:
#             # Strip leading/trailing whitespace and remove the numbering
#             line = line.strip()
#             # print(line)
#             if '. ' in line:
#                 topic = line.split('. ', 1)[1]
#                 print(topic)
#                 topics.append(topic)
#         return topics
#     except FileNotFoundError:
#         return "The file was not found."
#     except IOError:
#         return "An error occurred trying to read the file."

# def generate_dialogue(messages, topic):
#     dialogue_prompt = load_prompt_dict()['generate_dialogue']
#     dialogue_prompt = dialogue_prompt.format(topic)
#     messages.append({"role": "user", "content": dialogue_prompt})
#     response = model.inference_with_messages(messages)
#     messages.append({"role": "assistant", "content": response})
#     return response, messages


# def find_patterns(dialogue_text):
#     find_patterns_prompt = load_prompt_dict()['find_patterns']
#     messages = [{"role": "user", "content": dialogue_text + '\n\n' + find_patterns_prompt}]
#     response = model.inference_with_messages(messages)
#     return response


if __name__ == '__main__':
    main()
