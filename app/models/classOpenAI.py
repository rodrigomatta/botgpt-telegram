from openai import OpenAI

class OpenAIChatbot:
    def __init__(self, api_key, chatbot_instance):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.chatbot_instance = chatbot_instance # Store the Chatbot instance

    def gerar_resposta(self, prompt, modelo, temperatura):
        # Generate the response
        resposta = self.client.chat.completions.create(model=modelo,
                                                        messages=[
                                                            {"role": "system", "content": "Você é uma namorada disposta e carinhosa chamada Utena"},
                                                            {"role": "user", "content": prompt}
                                                        ],
                                                        temperature=temperatura)
        # Extract the response content
        response_content = resposta.choices[0].message.content
        
        # Calculate the number of tokens in the prompt and the response
        tokens_prompt = len(prompt.split())
        tokens_completion = len(response_content.split())
        
        # Call the armazenar_custo method to store the costs
        self.chatbot_instance.armazenar_custo(tokens_prompt, tokens_completion, modelo)
        
        return response_content