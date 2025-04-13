FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5000

# Comando corrigido
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]