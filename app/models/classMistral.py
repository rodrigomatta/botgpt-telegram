from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

class MistralChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = MistralClient(api_key=self.api_key)

    def gerar_resposta(self, prompt, modelo, temperatura):
        messages = [ChatMessage(role="user", content=prompt)]
        chat_response = self.client.chat(model=modelo, messages=messages, temperature=temperatura)
        return chat_response.choices[0].message.content