import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key'


# Function to make API call and track token usage
def get_response_and_track_tokens(prompt, model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150  # Adjust this based on your expected response length
    )
    usage = response['usage']
    prompt_tokens = usage['prompt_tokens']
    completion_tokens = usage['completion_tokens']
    total_tokens = usage['total_tokens']
    return response, prompt_tokens, completion_tokens, total_tokens


# List to store total tokens for each API call
token_usage = []

# Example prompts
prompts = [
    "What is the capital of France?",
    # Add more prompts as needed
]

# Making API calls and tracking token usage
for prompt in prompts:
    _, prompt_tokens, completion_tokens, total_tokens = get_response_and_track_tokens(prompt)
    token_usage.append(total_tokens)
    print(
        f"Prompt: {prompt}\nPrompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}, Total Tokens: {total_tokens}\n")

# Calculate average tokens used
average_tokens = sum(token_usage) / len(token_usage)
print(f"Average tokens used per API call: {average_tokens}")
