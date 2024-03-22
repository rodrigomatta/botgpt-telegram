import os
import time
import telebot
from dotenv import load_dotenv
import logging
from telegram.handlers.handlerCommands import HandlerCommands
from telegram.handlers.handlerCusto import HandlerCusto
from telegram.handlers.handlerReply import HandlerReply
from telegram.handlers.handlerModels import HandlerModels

class Telegram:
    def __init__(self):
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.bot = telebot.TeleBot(self.TELEGRAM_TOKEN)
        self.allowed_chat_id = int(os.getenv('TELEGRAM_ALLOWED_ID_CHAT'))
        self.handler_commands = HandlerCommands(self.bot, self.allowed_chat_id)
        self.handler_custo = HandlerCusto(self.bot, self.allowed_chat_id)
        self.handler_models = HandlerModels(self.bot, self.allowed_chat_id, self)
        self.modelo_selecionado = self.handler_models.modelo_selecionado
        self.assistente = self.handler_models.initialize_assistant(self.modelo_selecionado)
        self.handler_reply = HandlerReply(self.bot, self.allowed_chat_id, self.assistente, self.modelo_selecionado)
        self.add_handlers()

    def add_handlers(self):
        self.handler_commands.register_handlers()
        self.handler_custo.register_handlers()
        self.handler_models.register_handlers()
        self.handler_reply.register_handlers()

    def update_assistant(self, modelo_selecionado):
        use_openai = "gpt" in modelo_selecionado.lower()
        use_gemini = "gemini" in modelo_selecionado.lower()
        use_mistral = any(m in modelo_selecionado.lower() for m in ["mistral", "mixtral"])
        use_anthropic = "claude" in modelo_selecionado.lower()

        self.assistente.update_instance(modelo_selecionado, use_openai, use_gemini, use_mistral, use_anthropic)
        self.modelo_selecionado = modelo_selecionado
        self.handler_reply.modelo_selecionado = modelo_selecionado

    def main(self):
        while True:
            try:
                self.bot.polling(none_stop=True)
            except Exception as e:
                logging.error(f"Um erro inesperado ocorreu: {e}")
                time.sleep(10)