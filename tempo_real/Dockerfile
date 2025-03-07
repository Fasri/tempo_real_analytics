# Usar uma imagem base leve do Python
FROM python:3.10-slim

# Definir variáveis de ambiente para o Poetry
ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Instalar dependências do sistema para o Selenium (Firefox e Geckodriver)
RUN apt-get update && apt-get install -y firefox-esr \
    && apt-get clean

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Criar a pasta 'data' dentro do container
RUN mkdir -p /app/data

# Copiar arquivos de dependência primeiro
COPY pyproject.toml poetry.lock /app/

# Instalar dependências do projeto
RUN poetry install --no-root --only main

# Copiar o restante dos arquivos do projeto
COPY . /app

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
