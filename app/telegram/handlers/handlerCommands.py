from telegram.handlers.baseHandler import BaseHandler

class HandlerCommands(BaseHandler):
    def __init__(self, bot, allowed_chat_id):
        super().__init__(bot, allowed_chat_id)
        self.allowed_chat_id = allowed_chat_id

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_command(message):
            if message.chat.id != self.allowed_chat_id:
                return
            self.start(message)

    def start(self, message):
        if message.chat.id != self.allowed_chat_id:
            return
        # Mensagem de boas-vindas e instruções detalhadas
        welcome_message = """
        🚀 *Bem-vindo ao nosso Bot!* 🎉

        Estamos animados por você estar aqui! Aqui estão os comandos que você pode usar para interagir com o bot:

        - `/start`: 🔄 Inicia o bot e exibe esta mensagem de boas-vindas.
        - `/models`: 📚 Mostra a lista completa de todos os modelos disponíveis atualmente.
        - `/custo`: 💰 Informa os custos associados ao uso.

        Se precisar de ajuda ou tiver alguma dúvida, não hesite em entrar em contato. Estamos aqui para ajudar! 😊
        """

        # Envia a mensagem de boas-vindas e instruções para o usuário
        self.bot.reply_to(message, welcome_message)