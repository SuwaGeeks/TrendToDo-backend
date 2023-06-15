FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt