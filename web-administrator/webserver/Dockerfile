FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

ENV SERVER_PORT=8181

EXPOSE ${SERVER_PORT}

CMD ["python3", "app.py"]