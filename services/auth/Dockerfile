FROM python:3.11-slim

WORKDIR /opt/auth

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]