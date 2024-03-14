import json
import os
import time
import telebot
from dotenv import load_dotenv
import logging
from classChatbot import Chatbot

class Telegram:
    def __init__(self):
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.bot = telebot.TeleBot(self.TELEGRAM_TOKEN)
        self.modelo_selecionado = os.getenv('SELECTED_MODEL')
        self.assistente = self.initialize_gemini()
        self.assistente = self.initialize_mistral()
        self.allowed_chat_id = int(os.getenv('TELEGRAM_ALLOWED_ID_CHAT'))
        self.use_gemini = False
        self.use_mistral = False
        self.use_anthropic = False

    def initialize_gemini(self, use_gemini=False):
        return Chatbot(model=self.modelo_selecionado, use_gemini=use_gemini, use_mistral=False, use_anthropic=False) 

    def initialize_mistral(self, use_mistral=False): 
        return Chatbot(model=self.modelo_selecionado, use_gemini=False, use_mistral=use_mistral, use_anthropic=False)
    
    def initialize_anthropic(self, use_anthropic=False): 
        return Chatbot(model=self.modelo_selecionado, use_gemini=False, use_mistral=False, use_anthropic=use_anthropic)

    def start(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        self.bot.reply_to(message, 'Bot iniciado com sucesso!')

    def reply_message(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        response = self.assistente.gerar_resposta(message.text, self.modelo_selecionado)
        self.bot.reply_to(message, response)

    def enviar_modelos_disponiveis(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        modelos = self.carregar_modelos_do_arquivo()
        resposta = "Modelos disponíveis:\n" + "\n".join(modelos) + "\n\nPara selecionar um modelo, envie o comando /select_model seguido do nome do modelo desejado."
        
        self.bot.reply_to(message, resposta)

    def select_model_handler(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        model_name = message.text.split('/select_model ')[-1].strip()
        modelos_disponiveis = self.carregar_modelos_do_arquivo()
        
        if model_name in modelos_disponiveis:
            self.modelo_selecionado = model_name
            self.use_gemini = "gemini" in model_name
            self.use_anthropic = "claude" in model_name
            self.use_mistral = "mistral" in model_name or "mixtral" in model_name

            if self.use_gemini:
                self.assistente = self.initialize_gemini(use_gemini=True)
            elif self.use_mistral:
                self.assistente = self.initialize_mistral(use_mistral=True)
            elif self.use_anthropic:
                self.assistente = self.initialize_anthropic(use_anthropic=True)
            else:
                self.assistente = self.initialize_gemini(use_gemini=False)
            
            self.bot.reply_to(message, f"Modelo {model_name} selecionado com sucesso!")
        else:
            self.bot.reply_to(message, "Modelo inválido. Por favor, escolha um modelo válido da lista.")

    def carregar_modelos_do_arquivo(self):
        try:
            with open('models.json', 'r') as file:
                data = json.load(file)
            return [model['name'] for model in data['models']]
        except FileNotFoundError:
            logging.error("Arquivo models.json não encontrado.")
            return []
        
    def add_handlers(self):
        @self.bot.message_handler(commands=['start', 'models', 'select_model'])
        def handle_command(message):
            if message.text.startswith('/start'):
                self.start(message)
            elif message.text.startswith('/models'):
                self.enviar_modelos_disponiveis(message)
            elif message.text.startswith('/select_model'):
                self.select_model_handler(message)

        @self.bot.message_handler(commands=['custo'])
        def custo_handler(message):
            if message.chat.id != self.allowed_chat_id:
                return
            try:
                with open('custos.json', 'r') as file:
                    custos = json.load(file)
                    total_tokens_prompt = sum(item['tokens_prompt'] for item in custos)
                    total_tokens_completion = sum(item['tokens_completion'] for item in custos)
                    total_tokens = total_tokens_prompt + total_tokens_completion
                    custo_entrada = sum(item['custo_entrada'] for item in custos)
                    custo_saida = sum(item['custo_saida'] for item in custos)
                    custo_total = sum(item['custo_total'] for item in custos)
                    
                    resposta = (f"############ RELATÓRIO DE CUSTOS ############\n"
                                f"####### SOMENTE OPENAI E ANTHROPIC ##########\n\n"
                                f"Total de Tokens do prompt: {total_tokens_prompt}\n"
                                f"Total de Tokens da completion: {total_tokens_completion}\n"
                                f"Total de tokens Geral: {total_tokens}\n"
                                f"Custo de entrada: ${custo_entrada:.4f}\n"
                                f"Custo de saída: ${custo_saida:.4f}\n"
                                f"Custo total: ${custo_total:.4f}")
                    self.bot.reply_to(message, resposta)
            except FileNotFoundError:
                self.bot.reply_to(message, "Nenhum custo registrado até o momento.")

        @self.bot.message_handler(func=lambda message: True)
        def reply_handler(message):
            self.reply_message(message)

    def main(self):
        self.add_handlers()
        while True:
            try:
                self.bot.polling(none_stop=True)
            except Exception as e:
                logging.error(f"Ocorreu um erro não esperado: {e}")
                time.sleep(10)