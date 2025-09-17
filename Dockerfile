FROM python:3.11-slim
WORKDIR /app
# Instale dependências necessárias para monitoramento
COPY requirements.txt /app/requirements.txt
RUN pip install watchdog && pip install -r /app/requirements.txt
# Exponha a porta padrão (ajuste conforme sua aplicação)
EXPOSE 8000
# Comando padrão: será sobrescrito pelo docker-compose
CMD ["python", "main.py"]