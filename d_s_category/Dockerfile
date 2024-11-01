FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD . .

EXPOSE 8000

CMD ["uvicorn", "d_s_category:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]