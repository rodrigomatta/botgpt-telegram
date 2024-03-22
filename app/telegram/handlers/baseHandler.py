class BaseHandler:
    def __init__(self, bot, allowed_chat_id):
        self.bot = bot
        self.allowed_chat_id = allowed_chat_id