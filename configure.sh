 #!/bin/bash

# Obtém o diretório atual do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define a variável de ambiente PROJECT_PATH com o diretório do projeto
export PROJECT_PATH="$SCRIPT_DIR"

# Executa o docker-compose com o arquivo docker-compose.yaml no mesmo diretório
docker-compose up -d && docker logs botapi