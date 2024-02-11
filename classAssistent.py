import os
from openai import OpenAI
from dotenv import load_dotenv

class Assistente:
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0.7):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')  
        print("Chave de API da OpenAI:", self.api_key) 
        self.client = OpenAI(api_key=self.api_key)
        self.modelo = model
        self.temperatura = temperature


    def gerar_resposta(self, prompt):
        try:
            resposta = self.client.chat.completions.create(model=self.modelo,
                                                            messages=[
                                                                {"role": "system", "content": "Você é uma assistente virtual prestativa chamado Utena, que será responsavel em me ajudar a resolver problemas gerais."},
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

            # Calculando o custo estimado baseado no total de tokens utilizados
            custo_por_token_entrada =  0.0005  /  1000  # GPT4 $0.03, GPT3.5 $0.0005 por 1K tokens
            custo_por_token_saida =  0.0015 /  1000  # GPT4 $0.06, GPT3.5 $0.0015 por 1K tokens

            # Calculando custos separadamente
            custo_entrada = tokens_prompt * custo_por_token_entrada
            custo_saida = tokens_completion * custo_por_token_saida

            # Calculando o custo total
            custo_total = custo_entrada + custo_saida

            print(f"Custo de entrada: ${custo_entrada:.4f}")
            print(f"Custo de saída: ${custo_saida:.4f}")
            print(f"Custo total: ${custo_total:.4f}")

            return resposta.choices[0].message.content
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return "Desculpe, não consegui gerar uma resposta neste momento."