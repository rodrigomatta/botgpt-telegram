import os
import json
from dotenv import load_dotenv
from models.classMistral import MistralChatbot
from models.classAnthropic import AnthropicChatbot
from models.classOpenAI import OpenAIChatbot
from models.classGemini import GeminiChatbot

class Chatbot:
    def __init__(self, model, use_gemini=False, use_mistral=False, use_anthropic=False):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')  
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.modelo = model
        self.use_gemini = use_gemini
        self.use_mistral = use_mistral
        self.use_anthropic = use_anthropic
    
    def gerar_resposta(self, prompt, modelo, temperatura=0.7):
        if self.use_gemini:
            gemini_chatbot = GeminiChatbot(self.gemini_api_key)
            return gemini_chatbot.gerar_resposta(prompt, modelo, temperatura)
        elif self.use_mistral:
            mistral_chatbot = MistralChatbot(self.mistral_api_key)
            return mistral_chatbot.gerar_resposta(prompt, modelo, temperatura)
        elif self.use_anthropic:
            anthropic_chatbot = AnthropicChatbot(self.anthropic_api_key, self) # Pass self to AnthropicChatbot
            return anthropic_chatbot.gerar_resposta(prompt, modelo, temperatura)
        else:
            openai_chatbot = OpenAIChatbot(self.openai_api_key, self) # Pass self to OpenAIChatbot
            return openai_chatbot.gerar_resposta(prompt, modelo, temperatura)

    # verificar mais tarde a integração com os modelos
    def armazenar_custo(self, tokens_prompt, tokens_completion, modelo):
        # Calcula os custos com base no modelo utilizado
        with open('models.json', 'r') as file:
            models_data = json.load(file)
            for model in models_data['models']:
                if model['name'] == modelo:
                    custo_entrada = tokens_prompt * model['input_price'] / 1000
                    custo_saida = tokens_completion * model['output_price'] / 1000
                    break
            else:
                custo_entrada = custo_saida = 0  # Modelo não encontrado, custos zerados

        custo_total = custo_entrada + custo_saida

        # Armazena os dados no arquivo
        custo_data = {
            'tokens_prompt': tokens_prompt,
            'tokens_completion': tokens_completion,
            'custo_entrada': custo_entrada,
            'custo_saida': custo_saida,
            'custo_total': custo_total
        }
        try:
            with open('custos.json', 'r+') as file:
                data = json.load(file)
                data.append(custo_data)
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open('custos.json', 'w') as file:
                json.dump([custo_data], file, indent=4)