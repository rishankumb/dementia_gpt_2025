import json
import pandas as pd
import os

base_dir = 'results/Meta-Llama-3-8B-Instruct'

# Load JSON data from a file
with open(os.path.join(base_dir, 'all_topic_metrics.json'), 'r') as json_file:
    data = json.load(json_file)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Reset the index to include the topic as a column
df.reset_index(inplace=True)
df.rename(columns={'index': 'Topic'}, inplace=True)

# Sort the DataFrame by 'num_scores' in descending order
df.sort_values(by='average_score', ascending=False, inplace=True)

# Save the sorted DataFrame to a CSV file
df.to_csv(os.path.join(base_dir, 'output.csv'), index=False)
