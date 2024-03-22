# BotGPT for Telegram

Este projeto consiste em dois arquivos principais:

1. **classChatbot.py**: Implementa um chatbot capaz de gerar respostas com base em modelos de IA da OpenAI, Mistral, Gemini e Anthropic. O bot pode ser configurado para usar um ou mais desses serviços de IA para gerar respostas para prompts dados pelo usuário.

2. **classTelegram.py**: Implementa um bot para o aplicativo de mensagens Telegram que utiliza o chatbot implementado em classChatbot.py para gerar respostas. Ele também permite selecionar o modelo de IA a ser usado para gerar respostas.

## Requisitos

Para executar este projeto, você precisará de:

- Python 3.12.2
- Pacotes Python listados no arquivo `requirements.txt`
- Credenciais de API da OpenAI, Mistral, Gemini e Anthropic (veja o arquivo example.env)

## Instalação

1. Clone o repositório para o seu sistema local.
2. Instale os pacotes Python necessários executando `pip install -r requirements.txt`.
3. Renomeie o arquivo `example.env` para `.env` e preencha as credenciais de API necessárias.
4. Execute o arquivo `configure.sh` para iniciar a configuração do projeto.

## Uso

- Para Iniciar o bot do Telegram, envie /start para exibir a mensagem inicial ou alguma mensagem para interagir com o chatbot (por padrão, o modelo principal é o gemini-pro).
- Use o comando `/models` para ver os modelos disponíveis.
- Use o comando `/custo` para ver os custos de utilização das APIs Anthropic e OpenAI.

## Configuração Avançada

Você pode modificar as configurações do bot editando os arquivos `example.env` e `models.json` conforme necessário.

## Estrutura do Projeto

O projeto é organizado em torno de duas classes principais: `classChatbot.py` e `classTelegram.py`. A primeira implementa a lógica do chatbot, enquanto a segunda gerencia a interação com o Telegram. Além disso, o projeto inclui vários manipuladores (handlers) e classes auxiliares para lidar com diferentes comandos, interações do usuário e integração com modelos de IA.

### classChatbot.py

- **classChatbot.py**: Implementa a lógica principal do chatbot, permitindo a geração de respostas com base em modelos de IA da OpenAI, Mistral, Gemini e Anthropic.
- **classOpenAI.py**: Responsável pela integração com o modelo de IA OpenAI. Configura a conexão com a API do OpenAI utilizando uma chave de API fornecida e define uma função `gerar_resposta` que gera uma resposta com base em um prompt, modelo e temperatura fornecidos. Também calcula e armazena os custos associados à geração da resposta.
- **classMistral.py**: Responsável pela integração com o modelo de IA Mistral. Configura a conexão com a API do Mistral utilizando uma chave de API fornecida e define uma função `gerar_resposta` que gera uma resposta com base em um prompt, modelo e temperatura fornecidos.
- **classGemini.py**: Responsável pela integração com o modelo de IA Gemini. Configura a conexão com a API do Gemini utilizando uma chave de API fornecida e define uma função `gerar_resposta` que gera uma resposta com base em um prompt, modelo e temperatura fornecidos.
- **classAnthropic.py**: Responsável pela integração com o modelo de IA Anthropic. Configura a conexão com a API do Anthropic utilizando uma chave de API fornecida e define uma função `gerar_resposta` que gera uma resposta com base em um prompt, modelo e temperatura fornecidos. Além disso, calcula e armazena os custos associados à geração da resposta.

### classTelegram.py

- **classTelegram.py**: Gerencia a interação com o Telegram, utilizando a funcionalidade do chatbot para responder às mensagens dos usuários.

### Handlers

- **handlerModels.py**: Gerencia a seleção e atualização do modelo de IA a ser utilizado pelo chatbot.
- **handlerReply.py**: Lida com as mensagens recebidas e gera respostas com base no modelo de IA selecionado.
- **handlerCusto.py**: Fornece informações sobre os custos associados ao uso dos modelos de IA.

### Configuração

- **example.env**: Neste arquivo, você deve substituir `sua_chave_de_api_openai`, `sua_chave_de_api_mistral`, `sua_chave_de_api_anthropic`, `sua_chave_de_api_gemini`, `seu_token_de_bot_telegram`, `seu_id_habilitado_telegram`, e `nome_do_modelo_padrao` pelos valores reais que você obteve dos serviços correspondentes:
  - `OPENAI_API_KEY`: A chave de API fornecida pelo OpenAI para acessar seus serviços de IA.
  - `MISTRAL_API_KEY`: A chave de API fornecida pelo Mistral para acessar seus serviços de IA.
  - `ANTHROPIC_API_KEY`: A chave de API fornecida pelo Anthropic para acessar seus serviços de IA.
  - `GEMINI_API_KEY`: A chave de API fornecida pelo Gemini para acessar seus serviços de IA.
  - `TELEGRAM_TOKEN`: O token do seu bot do Telegram, necessário para que o bot possa interagir com a API do Telegram.
  - `TELEGRAM_ALLOWED_ID_CHAT`: O ID do chat do Telegram habilitado para interagir com o bot. Útil para restringir o acesso apenas a usuários específicos.
  - `SELECTED_MODEL`: O nome do modelo de IA padrão que o chatbot deve usar para gerar respostas.

### Arquivo `models.json`

O arquivo `models.json` contém informações sobre os modelos de IA disponíveis, incluindo o nome do modelo e os custos associados ao uso de cada modelo.

## Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue para discutir quaisquer mudanças importantes antes de enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).