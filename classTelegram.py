import os
import time
import telebot
from classAssistent import Assistente
from dotenv import load_dotenv
import logging

class Telegram:
    def __init__(self):
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        print("Token do Telegram:", self.TELEGRAM_TOKEN)  # Para debug
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.bot = telebot.TeleBot(self.TELEGRAM_TOKEN)  # Cria uma instância do bot
        self.assistente = Assistente()

    def start(self, message):
        self.bot.reply_to(message, 'Bot iniciado com sucesso! Envie-me uma mensagem e eu responderei.')
        logging.info('Bot iniciado com sucesso!')

    def reply_message(self, message):
        user_message = message.text
        response = self.assistente.gerar_resposta(user_message)  # Usa o Assistente para gerar a resposta
        print(f"Resposta: {response}")
        self.bot.reply_to(message, response)

    def add_handlers(self):
        @self.bot.message_handler(commands=['start'])  # Define um manipulador para o comando /start
        def handle_start(message):
            self.start(message)

        @self.bot.message_handler(func=lambda message: True)  # Define um manipulador para qualquer texto
        def handle_text(message):
            self.reply_message(message)

    def main(self):
        self.add_handlers()
        while True:
            try:
                self.bot.polling(none_stop=True)  # Inicia o polling
            except Exception as e:
                logging.error(f"Ocorreu um erro não esperado: {e}")
                time.sleep(10)

if __name__ == "__main__":
    telegram_bot = Telegram()
    telegram_bot.main()