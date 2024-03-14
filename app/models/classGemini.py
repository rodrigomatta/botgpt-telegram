import google.generativeai as genai

class GeminiChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def gerar_resposta(self, prompt, modelo, temperatura):
        model = genai.GenerativeModel(modelo, generation_config=genai.GenerationConfig(
            candidate_count=1,  
            temperature=temperatura,
        ))
        response = model.generate_content([prompt])
        return response.text