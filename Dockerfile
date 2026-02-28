FROM python:3.12-slim

WORKDIR /medicines_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Dependências do sistema para mysqlclient e crontab
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
         gcc \
         pkg-config \
         default-libmysqlclient-dev \
         cron \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

COPY ./cron /etc/cron.d/cron

# 1. Remove os finais de linha do Windows (\r)
# 2. Adiciona uma linha em branco no final para o cron funcionar
# 3. Ajusta as permissões e carrega no crontab
RUN sed -i 's/\r$//' /etc/cron.d/cron && \
    echo "" >> /etc/cron.d/cron && \
    chmod 0644 /etc/cron.d/cron && \
    crontab /etc/cron.d/cron

# Cria o arquivo de log antecipadamente para evitar erro de "No such file"
RUN touch /var/log/cron.log


EXPOSE 8000
