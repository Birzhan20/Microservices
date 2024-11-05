FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD . .

EXPOSE 8000

CMD ["python", "phys_jud.py"]