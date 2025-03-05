import os
import json
import re

import models

# model_name = 'meta-llama/Meta-Llama-3-8B-Instruct'
model_name = 'gpt-4'
model = models.OpenAIModel(model_name)

file_path = 'rq1_prompts/topics-gpt.txt'


def load_prompt_dict():
    prompt_dir = "rq1_prompts"
    prompt_type = "probing_prompts"
    contexts_json_path = os.path.join(prompt_dir, prompt_type + '.json')
    with open(contexts_json_path, 'r', encoding='utf-8') as f:
        prompt_dict = json.load(f)
    return prompt_dict


def main():
    turns = 2
    for i in range(1, turns):
        file_name = f"output_files_set_{i}"
        generate_output_files(file_name)

    print("All file sets created successfully.")


def generate_output_files(file_name):
    pattern_response, pattern_messages = list_pattern()
    pattern = r'\d+\.\s*(.*?)\:'
    pattern_matches = re.findall(pattern, pattern_response)
    print(pattern_matches)
    extracted_pattern = []
    for i, match in enumerate(pattern_matches):
        extracted_pattern.append(match)
    print(extracted_pattern)
    # topic_response, topic_messages = list_topics(pattern_messages.copy())
    # topic_matches = pattern.findall(topic_response)
    # extracted_topic = []
    # for i, match in enumerate(topic_matches):
    #     extracted_topic.append(match)
    extracted_topic = list_topics()
    # print("Line 31")
    # print(extracted_topic)
    # pattern2 = r'\d+\.\s*(.*?)'
    # pattern2 = r'\d+\.\s*([a-zA-Z]+)'
    pattern2 = r'\d+\.\s*([^\d\n]+)'

    for i, match in enumerate(extracted_topic):
        for j in range(1, 11):
            dialogue_response, dialogue_messages = generate_dialogue(pattern_messages.copy(), match)

            find_pattern_response = find_patterns(dialogue_response, extracted_pattern)
            find_pattern_response = find_pattern_response.strip("'")
            extracted_dialogue = find_pattern_response.split("', '")
            # extracted_dialogue = []
            # dialogue_matches = re.findall(pattern2, find_pattern_response)
            # print("Dialogues:", dialogue_matches)
            # dialogue_matches = [match.strip().rstrip('.') for match in dialogue_matches]
            # for k, matches in enumerate(dialogue_matches):
            #     extracted_dialogue.append(matches)
            extracted_dialogue_set = set(extracted_dialogue)
            extracted_pattern_set = set(extracted_pattern)
            pattern_match = extracted_dialogue_set.intersection(extracted_pattern_set)
            # patterns_not_match = extracted_pattern_set - extracted_dialogue_set

            score = len(pattern_match)

            if not os.path.exists(file_name):
                os.makedirs(file_name)
                print(f"Folder {file_name} created successfully.")
            else:
                print(f"Folder {file_name} already exists.")

            content = (f"Original pattern: {pattern_response}\n\n\n"
                       f"Processed pattern: {extracted_pattern}\n\n\n"
                       f"Original topic: {extracted_topic}\n\n\n"
                       f"Processed topic: {match}\n\n\n"
                       f"Dialogue: {dialogue_response}\n\n\n"
                       f"pattern response: {find_pattern_response}\n\n\n"
                       f"pattern response: {type(find_pattern_response)}\n\n\n"
                       f"Final pattern output: {extracted_dialogue}\n\n\n"
                       f"Score output: {score}\n")
            f_name = f"output_file_{i}_{j}"
            file_path_2 = os.path.join(file_name, f_name)
            with open(file_path_2, 'w') as file:
                file.write(content)
            print(f"File '{f_name}' created.")


def list_pattern(context=''):
    list_patterns_prompt = load_prompt_dict()['list_patterns']
    if context:
        list_patterns_prompt = context + "\n\n" + list_patterns_prompt
    messages = [{"role": "user", "content": str(list_patterns_prompt)}]
    response = model.inference_with_messages(messages)
    messages.append({"role": "assistant", "content": response})
    return response, messages


# def list_topics(messages):
#     topics_prompt = load_prompt_dict()['list_topics']
#     messages.append({"role": "user", "content": topics_prompt})
#     response = model.inference_with_messages(messages)
#     messages.append({"role": "assistant", "content": response})
#     return response, messages

def list_topics():
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        topics = []
        for line in content:
            # Strip leading/trailing whitespace and remove the numbering
            line = line.strip()
            # print(line)
            if '. ' in line:
                topic = line.split('. ', 1)[1]
                print(topic)
                topics.append(topic)
        return topics
    except FileNotFoundError:
        return "The file was not found."
    except IOError:
        return "An error occurred trying to read the file."


def generate_dialogue(messages, topic):
    dialogue_prompt = load_prompt_dict()['generate_dialogue']
    dialogue_prompt = dialogue_prompt.format(topic)
    messages.append({"role": "user", "content": dialogue_prompt})
    response = model.inference_with_messages(messages)
    messages.append({"role": "assistant", "content": response})
    return response, messages


def find_patterns(dialogue_text, extracted_pattern):
    find_patterns_prompt = load_prompt_dict()['find_patterns']
    find_patterns_prompt = find_patterns_prompt.format(extracted_pattern)
    messages = [{"role": "user", "content": dialogue_text + '\n\n' + find_patterns_prompt}]
    response = model.inference_with_messages(messages)
    return response


if __name__ == '__main__':
    main()
