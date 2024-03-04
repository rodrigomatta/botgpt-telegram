# BotGPT for Telegram

Este projeto consiste em dois arquivos principais:

1. **classChatbot.py**: Implementa um chatbot capaz de gerar respostas com base em modelos de IA da OpenAI, Mistral e Gemini. O bot pode ser configurado para usar um ou mais desses serviços de IA para gerar respostas para prompts dados pelo usuário.

2. **classTelegram.py**: Implementa um bot para o aplicativo de mensagens Telegram que utiliza o chatbot implementado em classChatbot.py para gerar respostas. Ele também permite selecionar o modelo de IA a ser usado para gerar respostas.

## Requisitos

Para executar este projeto, você precisará de:

- Python 3.12
- Pacotes Python listados no arquivo `requirements.txt`
- Credenciais de API da OpenAI, Mistral e Gemini (veja o arquivo example.env)

## Instalação

1. Clone o repositório para o seu sistema local.
2. Instale os pacotes Python necessários executando `pip install -r requirements.txt`.
3. Renomeie o arquivo `example.env` para `.env` e preencha as credenciais de API necessárias.
4. Execute o arquivo `configure.sh` para iniciar a configuração do projeto.

## Uso

- Para Iniciar o bot do Telegram, envie /start ou alguma mensagen para interagir com o chatbot (por padrão o modelo principal é gpt-3.5-turbo).
- Use o comando `/models` para ver os modelos disponíveis.
- Use o comando `/select_model` seguido pelo nome do modelo desejado para selecionar um modelo específico.

## Configuração Avançada

Você pode modificar as configurações do bot editando os arquivos `classChatbot.py`, `classTelegram.py`, e `models.json` conforme necessário.

## Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue para discutir quaisquer mudanças importantes antes de enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).