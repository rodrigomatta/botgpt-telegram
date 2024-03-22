from telegram.handlers.baseHandler import BaseHandler

class HandlerReply(BaseHandler):
    def __init__(self, bot, allowed_chat_id, assistente, modelo_selecionado):
        super().__init__(bot, allowed_chat_id)
        self.assistente = assistente
        self.modelo_selecionado = modelo_selecionado

    def register_handlers(self):
        @self.bot.message_handler(func=lambda message: True)
        def reply_handler(message):
            self.reply_message(message)

    def reply_message(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        response = self.assistente.gerar_resposta(message.text, self.modelo_selecionado)
        if not response:
            response = "Desculpe, eu não consegui gerar uma resposta."
        self.bot.reply_to(message, response)