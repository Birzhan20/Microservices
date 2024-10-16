FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD . .

EXPOSE 8050

CMD ["uvicorn", "sigma:app", "--host", "0.0.0.0", "--port", "8050", "--proxy-headers"]

# Флаг --proxy-headers позволяет приложению видеть реальный IP-адрес клиента и протокол
#(HTTP/HTTPS), когда оно работает за прокси-сервером.