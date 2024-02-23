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
        self.modelo_selecionado = "gpt-3.5-turbo-0125"
        self.assistente = self.initialize_openai()
        self.allowed_chat_id = 00000 # Definindo o ID do chat permitido

    def initialize_openai(self, use_gemini=False):
        return Chatbot(model=self.modelo_selecionado, use_gemini=use_gemini)

    def start(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        self.bot.reply_to(message, 'Bot iniciado com sucesso!')

    def reply_message(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        response = self.assistente.gerar_resposta(message.text)
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
            # Aqui verificamos se o modelo selecionado é um modelo Gemini
            self.use_gemini = "gemini" in model_name
            # Atualizamos a instância do assistente com a nova configuração
            self.assistente = self.initialize_openai(use_gemini=self.use_gemini)
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
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            self.start(message)

        @self.bot.message_handler(commands=['models'])
        def models_handler(message):
            self.enviar_modelos_disponiveis(message)

        @self.bot.message_handler(commands=['select_model'])
        def select_model_handler(message):
            self.select_model_handler(message)
        
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