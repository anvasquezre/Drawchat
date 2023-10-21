FROM python:3.10.13 as base

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install 'pydantic[email]'
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000
WORKDIR /app


FROM base as build
ENTRYPOINT ["uvicorn", "main:api", "--host", "0.0.0.0"]

