FROM registry.opensuse.org/opensuse/leap:15.5
ARG CONTAINER_USERID

# Atualiza a lista de pacotes e instala as dependências necessárias
RUN zypper -n --gpg-auto-import-keys refresh && \
    zypper -n install -y gcc libffi-devel libopenssl-devel zlib-devel wget tar gzip make && \
    wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz && \
    tar -xf Python-3.12.2.tgz && \
    cd Python-3.12.2 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf Python-3.12.2* && \
    zypper -n remove -y gcc libffi-devel libopenssl-devel zlib-devel wget tar gzip make && \
    zypper clean --all

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos
COPY requirements.txt .

# Copia o conteúdo da pasta app do seu projeto para /app no contêiner
COPY app /app

# Instala as dependências do projeto
RUN pip3.12 install --no-cache-dir -r requirements.txt

# Comando padrão
CMD ["python3.12", "main.py"]
