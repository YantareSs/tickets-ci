FROM python:3.12.7-slim
WORKDIR /app
COPY tickets.py README.md tickets.csv.example ./
ENV APP_PORT=8103
ENTRYPOINT ["python", "tickets.py"]