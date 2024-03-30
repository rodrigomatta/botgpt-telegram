import json
from telegram.handlers.baseHandler import BaseHandler

class HandlerAdmin(BaseHandler):
    def __init__(self, bot, allowed_chat_id, allowed_tokens):
        super().__init__(bot, allowed_chat_id, allowed_tokens)
        self.allowed_chat_id = allowed_chat_id
        self.allowed_tokens = allowed_tokens

    def register_handlers(self):
        @self.bot.message_handler(commands=['admin'])
        def admin_handler(message):
            command_parts = message.text.split()
            if message.chat.id == self.allowed_chat_id:
                self.handle_admin_command(message, command_parts)
            elif 'mytoken' in command_parts:
                self.handle_mytoken_command(message)
            else:
                self.handle_unauthorized_access(message)

    def handle_admin_command(self, message, command_parts):
        if 'token' in command_parts:
            self.handle_token_command(message, command_parts)
        elif 'help' in command_parts:
            self.handle_help_command(message)
        else:
            self.bot.send_message(message.chat.id, "Comando não encontrado! O formato correto é /admin <command>. Utilize `/admin help` para obter ajuda.")

    def handle_token_command(self, message, command_parts):
        if len(command_parts) > 2:
            token = command_parts[2]
            tokens_data = self.load_tokens_data()
            if token in tokens_data['tokens']:
                self.bot.send_message(message.chat.id, f"O token {token} já existe.")
            else:
                tokens_data['tokens'].append(token)
                self.save_tokens_data(tokens_data)
                self.bot.send_message(message.chat.id, "Token salvo com sucesso e acesso liberado.")
        else:
            self.bot.send_message(message.chat.id, "Por favor, forneça o token após o comando `/admin token`.")

    def handle_help_command(self, message):
        help_message = """
        🚀 *Bem-vindo a Administração do nosso Bot!* 🎉

        - `/admin help`:❓Este comando exibe esta mensagem de ajuda.
        - `/admin token <token>`: 🔑 Salva um novo token de usuario do telegram para liberar acesso ao bot. Substitua `<token>` pelo token real que você deseja salvar.
        - `/admin mytoken`: 🔍 Consulta o Chat ID do usuário atual para utiliza-lo em `/admin mytoken`.

        Se precisar de ajuda ou tiver alguma dúvida, não hesite em entrar em contato. Estamos aqui para ajudar! 😊
        """
        self.bot.send_message(message.chat.id, help_message, parse_mode='Markdown')

    def handle_mytoken_command(self, message):
        self.bot.send_message(message.chat.id, f"Chat ID do usuário: {message.chat.id}")

    def handle_unauthorized_access(self, message):
        self.bot.send_message(message.chat.id, "Acesso negado. Você não é um administrador autorizado, para vizualizar o seu token rode o comando: `/admin mytoken`")

    def load_tokens_data(self):
        try:
            with open('telegram_token.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'tokens': []}

    def save_tokens_data(self, tokens_data):
        with open('telegram_token.json', 'w') as f:
            json.dump(tokens_data, f)