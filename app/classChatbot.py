import os
from openai import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai

class Chatbot:
    def __init__(self, model, temperature=0.7, use_gemini=False):
        load_dotenv()
        self.prompt_system = "Você é uma namorada disposta e carinhosa chamada Utena"
        self.openai_api_key = os.getenv('OPENAI_API_KEY')  
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.client = OpenAI(api_key=self.openai_api_key)
        self.modelo = model
        self.temperatura = temperature
        self.use_gemini = use_gemini
        
        if self.use_gemini:
            genai.configure(api_key=self.gemini_api_key)
        
    def gerar_resposta(self, prompt):
        if self.use_gemini:
            return self.gerar_resposta_gemini(prompt)
        else:
            return self.gerar_resposta_openai(prompt)

    def gerar_resposta_gemini(self, prompt):
        if not self.use_gemini:
            return "Configuração para Gemini não ativada."
        try:
            model = genai.GenerativeModel(self.modelo)
            response = model.generate_content([self.prompt_system, prompt])
            return response.text
        except Exception as e:
            print(f"Ocorreu um erro ao gerar resposta com Gemini: {e}")
            return "Desculpe, não consegui gerar uma resposta com Gemini neste momento."

    def gerar_resposta_openai(self, prompt):
        try:
            resposta = self.client.chat.completions.create(model=self.modelo,
                                                            messages=[
                                                                {"role": "system", "content": self.prompt_system},
                                                                {"role": "user", "content": prompt}
                                                            ],
                                                            temperature=self.temperatura)
            uso = resposta.usage
            tokens_prompt = uso.prompt_tokens
            tokens_completion = uso.completion_tokens
            total_tokens = uso.total_tokens

            print("---------------------------------------------------")
            print(f"Tokens do prompt: {tokens_prompt}")
            print(f"Tokens da completion: {tokens_completion}")
            print(f"Total de tokens: {total_tokens}")

            custo_por_token_entrada =  0.0005  /  1000
            custo_por_token_saida =  0.0015 /  1000

            custo_entrada = tokens_prompt * custo_por_token_entrada
            custo_saida = tokens_completion * custo_por_token_saida

            custo_total = custo_entrada + custo_saida

            print(f"Custo de entrada: ${custo_entrada:.4f}")
            print(f"Custo de saída: ${custo_saida:.4f}")
            print(f"Custo total: ${custo_total:.4f}")

            return resposta.choices[0].message.content
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return "Desculpe, não consegui gerar uma resposta neste momento."