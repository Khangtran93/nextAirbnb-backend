FROM python:3.10.12-slim-bullseye
WORKDIR /usr/src/enbnb_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/enbnb_backend/entrypoint.sh 
RUN chmod +x /usr/src/enbnb_backend/entrypoint.sh

COPY . .

ENTRYPOINT [ "/usr/src/enbnb_backend/entrypoint.sh" ]