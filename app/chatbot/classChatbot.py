import logging
import os
import json
from dotenv import load_dotenv
from chatbot.models.classMistral import MistralChatbot
from chatbot.models.classAnthropic import AnthropicChatbot
from chatbot.models.classOpenAI import OpenAIChatbot
from chatbot.models.classGemini import GeminiChatbot

class Chatbot:
    def __init__(self, model, use_openai, use_gemini, use_mistral, use_anthropic):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')  
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.modelo = model
        self.use_openai = use_openai
        self.use_gemini = use_gemini
        self.use_mistral = use_mistral
        self.use_anthropic = use_anthropic
        self.update_instance(model, use_openai, use_gemini, use_mistral, use_anthropic)
 
    def update_instance(self, model, use_openai, use_gemini, use_mistral, use_anthropic):
        logging.debug(f"Flags: use_openai={use_openai}, use_gemini={use_gemini}, use_mistral={use_mistral}, use_anthropic={use_anthropic}")
        if use_gemini:
            self.instance = GeminiChatbot(self.gemini_api_key)
            logging.debug(f"Instance set to GeminiChatbot: {self.instance}")
        elif use_openai:
            self.instance = OpenAIChatbot(self.openai_api_key, self)
            logging.debug(f"Instance set to OpenAIChatbot: {self.instance}")
        elif use_mistral:
            self.instance = MistralChatbot(self.mistral_api_key)
            logging.debug(f"Instance set to MistralChatbot: {self.instance}")
        elif use_anthropic:
            self.instance = AnthropicChatbot(self.anthropic_api_key, self)
            logging.debug(f"Instance set to AnthropicChatbot: {self.instance}")
            
    def gerar_resposta(self, prompt, modelo, temperatura=0.7):
        try:
            return self.instance.gerar_resposta(prompt, modelo, temperatura)
        except Exception as e:
            logging.error(f"Erro ao gerar resposta com o modelo {modelo}: {e}")
            return "Desculpe, houve um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."

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
