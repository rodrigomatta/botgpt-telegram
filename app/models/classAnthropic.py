import anthropic

class AnthropicChatbot:
    def __init__(self, api_key, chatbot_instance):
        # Initialize the Anthropic client with the provided API key
        self.api_key = api_key
        self.client = anthropic.Client(api_key=self.api_key)
        self.chatbot_instance = chatbot_instance # Store the Chatbot instance

    def gerar_resposta(self, prompt, modelo, temperatura):
        # Generate the response
        resposta = self.client.messages.create(
            model=modelo,
            max_tokens=4096,
            system="Você é uma namorada disposta e carinhosa chamada Utena",
            messages=[ 
                {"role": "user", "content": prompt}
            ],
            temperature=temperatura
        )
        # Extract the response content
        response_content = resposta.content[0].text
        
        # Calculate the number of tokens in the prompt and the response
        tokens_prompt = len(prompt.split())
        tokens_completion = len(response_content.split())
        
        # Call the armazenar_custo method to store the costs
        self.chatbot_instance.armazenar_custo(tokens_prompt, tokens_completion, modelo)
        
        return response_content