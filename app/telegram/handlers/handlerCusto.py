import json
from telegram.handlers.baseHandler import BaseHandler

class HandlerCusto(BaseHandler):
    def __init__(self, bot, allowed_chat_id, allowed_tokens):
        super().__init__(bot, allowed_chat_id, allowed_tokens)
        self.allowed_chat_id = allowed_chat_id
        self.allowed_tokens = allowed_tokens

    def register_handlers(self):
        @self.bot.message_handler(commands=['custo'])
        def custo_handler(message):
            if message.chat.id != self.allowed_chat_id and message.chat.id not in self.allowed_tokens:
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
                    
                    resposta = (f"## RELATÓRIO DE CUSTOS ##\n"
                                f"## SOMENTE OPENAI E ANTHROPIC ##\n\n"
                                f"Total de Tokens do prompt: {total_tokens_prompt}\n"
                                f"Total de Tokens da completion: {total_tokens_completion}\n"
                                f"Total de tokens Geral: {total_tokens}\n"
                                f"Custo de entrada: ${custo_entrada:.4f}\n"
                                f"Custo de saída: ${custo_saida:.4f}\n"
                                f"Custo total: ${custo_total:.4f}")
                    self.bot.reply_to(message, resposta)
            except FileNotFoundError:
                self.bot.reply_to(message, "Nenhum custo registrado até o momento.")