FROM python:3.9

WORKDIR /back-end

COPY ./requirements.txt /back-end/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /back-end/requirements.txt

COPY ./ /back-end

ENV SERVER_PORT=8181

EXPOSE ${SERVER_PORT}

CMD ["python3", "app.py"]