import models


class Chatbot:
    def __init__(self, system_prompt, model_name):
        self.model = models.OpenAIModel(model_name)
        self.system_prompt = system_prompt
        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

    def chat(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = self.model.inference_with_messages(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response
