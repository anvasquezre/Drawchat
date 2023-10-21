FROM python:3.10.13 as base

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install 'pydantic[email]'
RUN pip install -r requirements.txt

COPY . /dashboard

EXPOSE 8051
WORKDIR /dashboard


FROM base as build
ENTRYPOINT ["streamlit", "run", "main.py" , "--server.port", "8051", "--server.address", "0.0.0.0"]

