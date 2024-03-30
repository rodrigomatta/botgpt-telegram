import json
import logging
import os
from chatbot.classChatbot import Chatbot
from telegram.handlers.baseHandler import BaseHandler
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class HandlerModels(BaseHandler):
    def __init__(self, bot, allowed_chat_id, allowed_tokens, telegram_instance):
        super().__init__(bot, allowed_chat_id, allowed_tokens)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        self.telegram_instance = telegram_instance
        self.allowed_tokens = allowed_tokens
        self.modelo_selecionado = os.getenv('SELECTED_MODEL')

    def initialize_assistant(self, model_name):
        use_openai = "gpt" in model_name.lower() 
        use_gemini = "gemini" in model_name.lower()
        use_mistral = any(m in model_name.lower() for m in ["mistral", "mixtral"])  
        use_anthropic = "claude" in model_name.lower()

        return Chatbot(model=model_name, use_openai=use_openai, use_gemini=use_gemini,
                    use_mistral=use_mistral, use_anthropic=use_anthropic)

    def register_handlers(self):
        @self.bot.message_handler(commands=['models'])
        def handle_command(message):
            if message.text.startswith('/models'):
                self.send_available_models(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            model_name = call.data
            available_models = self.load_models_from_file()

            if model_name in available_models:
                self.telegram_instance.update_assistant(model_name)
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           text=f"Modelo {model_name} selecionado com suscesso!")
            else:
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           text="modelo invalido. Por favor selecione um modelo válido na lista.")

    def send_available_models(self, message):
        if message.chat.id != self.allowed_chat_id and message.chat.id not in self.allowed_tokens:
            return

        models = self.load_models_from_file()
        keyboard = InlineKeyboardMarkup(row_width=2)
        for model in models:
            keyboard.add(InlineKeyboardButton(text=model, callback_data=model))

        response = "Selecione um dos modelos disponiveis"
        self.bot.reply_to(message, response, reply_markup=keyboard)

    def load_models_from_file(self):
        try:
            with open('models.json', 'r') as file:
                data = json.load(file)
            return [model['name'] for model in data['models']]
        except FileNotFoundError:
            logging.error("models.json arquivo não encontrado.")
            return []