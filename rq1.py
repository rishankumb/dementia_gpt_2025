import os
import json
import re
from glob import glob

import models

# model_name = 'meta-llama/Meta-Llama-3-8B-Instruct'
# model_name = 'meta-llama/Meta-Llama-3-70B-Instruct'
# model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
# model_name = 'meta-llama/Llama-2-7b-chat-hf'
# model = models.LLM(model_name)

model_name = 'gpt-3.5-turbo-0125'
# model_name = 'gpt-4o-2024-05-13'
model = models.OpenAIModel(model_name)


def load_prompt_dict():
    prompt_dir = "rq1_prompts"
    prompt_type = "probing_prompts"
    contexts_json_path = os.path.join(prompt_dir, prompt_type + '.json')
    with open(contexts_json_path, 'r', encoding='utf-8') as f:
        prompt_dict = json.load(f)
    return prompt_dict


def main():
    # save_path = f"output_files/{model_name.split('/')[-1]}"
    # generate_output_files(save_path)

    save_path = f"pattern_eval/{model_name.split('/')[-1]}"
    eval_pattern_context(save_path)
    # cal_iou(save_path)


def load_context():
    with open('rq1_prompts/context.txt', 'r', encoding='utf-8') as f:
        context = f.read()
    return context


def intersection_over_union(set1, set2):
    # Convert the inputs to sets
    set1 = set(set1)
    set2 = set(set2)

    # Calculate intersection and union
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # Calculate IoU
    iou = len(intersection) / len(union)

    return iou


def cal_iou(save_path):
    pattern_list_no_context = set()
    json_path_list = glob(os.path.join(save_path, 'pattern_no_context_*.json'))
    for json_path in json_path_list:
        with open(json_path, 'r', encoding='utf-8') as f:
            save_dicts = json.load(f)
        pattern_list_no_context.update(save_dicts['pattern'])

    pattern_list_context = set()
    json_path_list = glob(os.path.join(save_path, 'pattern_with_context_*.json'))
    for json_path in json_path_list:
        with open(json_path, 'r', encoding='utf-8') as f:
            save_dicts = json.load(f)
        pattern_list_context.update(save_dicts['pattern'])

    iou = intersection_over_union(pattern_list_no_context, pattern_list_context)
    print(iou)
    with open(os.path.join(save_path, f"iou.txt"), 'w', encoding='utf-8') as f:
        f.write(str(iou))


def eval_pattern_context(save_path):

    os.makedirs(save_path, exist_ok=True)

    pattern_list_no_context = set()
    pattern_list_context = set()

    context = load_context()
    print(context)

    for i in range(10):
        pattern_response, pattern_messages = list_pattern()
        pattern_list = extract_with_re(pattern_response)
        pattern_list_no_context.update(pattern_list)
        pattern_dict = {'chat': pattern_messages, 'pattern': pattern_list}
        with open(os.path.join(save_path, f"pattern_no_context_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(pattern_dict, f)

    for i in range(10):
        pattern_response, pattern_messages = list_pattern(context)
        pattern_list = extract_with_re(pattern_response)
        pattern_list_context.update(pattern_list)
        pattern_dict = {'chat': pattern_messages, 'pattern': pattern_list}
        with open(os.path.join(save_path, f"pattern_with_context_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(pattern_dict, f)

    iou = intersection_over_union(pattern_list_no_context, pattern_list_context)
    print(iou)
    with open(os.path.join(save_path, f"iou.txt"), 'w', encoding='utf-8') as f:
        f.write(str(iou))


def generate_output_files(model_output_path):
    os.makedirs(model_output_path, exist_ok=True)

    pattern_response, pattern_messages = list_pattern()
    extracted_pattern = extract_with_re(pattern_response)
    with open(os.path.join(model_output_path, 'patterns.json'), 'w', encoding='utf-8') as f:
        json.dump(extracted_pattern, f, ensure_ascii=False, indent=4)

    topic_response, topic_messages = list_topics(pattern_messages.copy())
    extracted_topic = extract_with_re(topic_response)
    with open(os.path.join(model_output_path, 'topics.json'), 'w', encoding='utf-8') as f:
        json.dump(extracted_topic, f, ensure_ascii=False, indent=4)
    # extracted_topic = list_topics(pattern_messages)
    # print("Line 31")
    # print(extracted_topic)

    for i, match in enumerate(extracted_topic):
        for j in range(1, 11):
            dialogue_response, dialogue_messages = generate_dialogue(pattern_messages.copy(), match)

            find_pattern_response = find_patterns(dialogue_messages)
            find_pattern_response = find_pattern_response.replace('*', '')

            extracted_dialogue = extract_with_re(find_pattern_response)
            extracted_dialogue_set = set(extracted_dialogue)
            extracted_pattern_set = set(extracted_pattern)

            patterns_not_match = extracted_pattern_set - extracted_dialogue_set
            score = 20 - len(patterns_not_match)

            content = (f"Original pattern: {pattern_response}\n\n\n"
                       f"Processed pattern: {extracted_pattern}\n\n\n"
                       f"Original topic: {extracted_topic}\n\n\n"
                       f"Processed topic: {match}\n\n\n"
                       f"Dialogue: {dialogue_response}\n\n\n"
                       f"Dialogue pattern: {find_pattern_response}\n\n\n"
                       f"Final pattern output: {extracted_dialogue}\n\n\n"
                       f"Score output: {score}\n")
            f_name = f"output_file_{i}_{j}.txt"
            file_path_2 = os.path.join(model_output_path, f_name)
            with open(file_path_2, 'w') as file:
                file.write(content)
            print(f"File '{f_name}' created.")


def extract_with_re(llm_response):
    re_pattern = re.compile(r".*\d+\.\s([^\n:\[\]\d]+):")
    llm_response = llm_response.replace('*', '')
    pattern_matches = re_pattern.findall(llm_response)
    extracted_pattern = []
    for i, match in enumerate(pattern_matches):
        extracted_pattern.append(match)
    return extracted_pattern


def list_pattern(context=''):
    list_patterns_prompt = load_prompt_dict()['list_patterns']
    if context:
        list_patterns_prompt = context + "\n\n" + list_patterns_prompt
    messages = [{"role": "user", "content": str(list_patterns_prompt)}]
    response = model.inference_with_messages(messages)
    messages.append({"role": "assistant", "content": response})
    return response, messages


def list_topics(messages):
    topics_prompt = load_prompt_dict()['list_topics']
    messages.append({"role": "user", "content": topics_prompt})
    response = model.inference_with_messages(messages)
    messages.append({"role": "assistant", "content": response})
    return response, messages


def generate_dialogue(messages, topic):
    dialogue_prompt = load_prompt_dict()['generate_dialogue']
    dialogue_prompt = dialogue_prompt.format(topic)
    messages.append({"role": "user", "content": dialogue_prompt})
    response = model.inference_with_messages(messages)
    messages.append({"role": "assistant", "content": response})
    return response, messages


def find_patterns(messages):
    find_patterns_prompt = load_prompt_dict()['find_patterns']
    messages.append({"role": "user", "content": find_patterns_prompt})
    response = model.inference_with_messages(messages)
    return response


if __name__ == '__main__':
    main()
