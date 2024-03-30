import logging
from telegram.handlers.baseHandler import BaseHandler

class HandlerReply(BaseHandler):
    def __init__(self, bot, allowed_chat_id, allowed_tokens, assistente, modelo_selecionado):
        super().__init__(bot, allowed_chat_id, allowed_tokens)
        self.assistente = assistente
        self.modelo_selecionado = modelo_selecionado

    def register_handlers(self):
        @self.bot.message_handler(func=lambda message: True)
        def reply_handler(message):
            self.reply_message(message)

    def reply_message(self, message):
        if message.chat.id != self.allowed_chat_id and message.chat.id not in self.allowed_tokens:
            logging.error(f"Mensagem de usuário não autorizado recebida. ID do chat: {message.chat.id}")
            return
        response = self.assistente.gerar_resposta(message.text, self.modelo_selecionado)
        if not response:
            response = "Desculpe, eu não consegui gerar uma resposta no momento."
        response = self.ajustar_resposta(response)
        self.bot.reply_to(message, response, parse_mode='Markdown')

    def ajustar_resposta(self, resposta):
        resposta_ajustada = resposta.replace('*', '').replace('_', '')
        return resposta_ajustada