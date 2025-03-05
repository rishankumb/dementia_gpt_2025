import os
import re
import json
from statistics import mean, variance


model_name = 'Meta-Llama-3-8B-Instruct'


# Function to extract topic and score from a given file
def extract_topic_and_score_from_file(file_path):
    print(f"Extracting data from file: {file_path}")
    topic = None
    score = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if topic is None:  # Assuming the topic appears first in the file
                    topic_match = re.search(r'Processed topic: (.+)', line)
                    if topic_match:
                        topic = topic_match.group(1)
                if score is None:
                    score_match = re.search(r'Score output: (\d+(\.\d+)?)', line)
                    if score_match:
                        score = float(score_match.group(1))
                if topic and score:
                    break
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return topic, score


# Function to traverse directories and process files
def extract_data_from_directory(root_dir):
    print(f"Traversing directory: {root_dir}")
    output_data = {}
    topic_score_map = {}
    for subdir, _, files in os.walk(root_dir):
        subdir_name = os.path.basename(subdir)
        output_data[subdir_name] = {}
        for file in files:
            file_path = os.path.join(subdir, file)
            topic, score = extract_topic_and_score_from_file(file_path)
            if topic and score is not None:
                output_data[subdir_name][file] = {
                    "Topic": topic,
                    "Score": score
                }
                if topic not in topic_score_map:
                    topic_score_map[topic] = []
                topic_score_map[topic].append(score)
            else:
                output_data[subdir_name][file] = {
                    "Topic": "N/A",
                    "Score": "N/A"
                }
    return output_data, topic_score_map


# Function to calculate statistics for each topic and rank them
def calculate_topic_statistics(topic_score_map):
    topic_metrics = {}
    for topic, scores in topic_score_map.items():
        avg_score = mean(scores)
        num_scores = len(scores)
        var_score = variance(scores) if len(scores) > 1 else 0.0  # variance requires at least two data points
        min_score = min(scores)
        max_score = max(scores)
        composite_metric = avg_score + num_scores  # Adjust weight as needed

        topic_metrics[topic] = {
            "average_score": avg_score,
            "num_scores": num_scores,
            "variance": var_score,
            "min_score": min_score,
            "max_score": max_score,
            "composite_metric": composite_metric
        }

    # Sort topics based on the composite metric in descending order
    ranked_topics = sorted(topic_metrics.items(), key=lambda x: x[1]["composite_metric"], reverse=True)[:10]

    return ranked_topics, topic_metrics


def main():
    print("Starting data extraction...")
    # Specify the root directory
    root_directory = os.path.join('output_files', model_name)
    result_dir = os.path.join('results', model_name)
    os.makedirs(result_dir, exist_ok=True)

    # Extract data
    data, topic_score_map = extract_data_from_directory(root_directory)

    # Print extracted data
    print("Extracted Data:")
    print(json.dumps(data, indent=4))

    # Save the extracted data to an output file
    output_file = os.path.join(result_dir, 'extracted_data.json')
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {output_file}")

    # Prepare and save the topic-score map to another output file
    topic_score_output = {topic: ", ".join(map(str, scores)) for topic, scores in topic_score_map.items()}
    topic_score_file = os.path.join(result_dir, 'topic_scores.json')
    with open(topic_score_file, 'w') as file:
        json.dump(topic_score_output, file, indent=4)
    print(f"Topic scores saved to {topic_score_file}")

    # Calculate and save the top 10 ranked topics by the composite metric
    ranked_topics, topic_metrics = calculate_topic_statistics(topic_score_map)
    ranked_topics_output = {
        topic: {
            "average_score": round(metrics["average_score"], 2),
            "num_scores": metrics["num_scores"],
            "variance": round(metrics["variance"], 2),
            "min_score": round(metrics["min_score"], 2),
            "max_score": round(metrics["max_score"], 2)
            # "composite_metric": round(metrics["composite_metric"], 2)
        }
        for topic, metrics in ranked_topics
    }
    ranked_topics_file = os.path.join(result_dir, 'ranked_topics.json')
    with open(ranked_topics_file, 'w') as file:
        json.dump(ranked_topics_output, file, indent=4)
    print(f"Ranked topics saved to {ranked_topics_file}")

    # Save all topic metrics to a separate file
    topic_metrics_file = os.path.join(result_dir, 'all_topic_metrics.json')
    with open(topic_metrics_file, 'w') as file:
        json.dump(topic_metrics, file, indent=4)
    print(f"All topic metrics saved to {topic_metrics_file}")


if __name__ == '__main__':
    main()
