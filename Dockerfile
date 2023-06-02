FROM python:3.9-slim

# Update and install system packages
RUN apt-get update -y && \
  apt-get install -y git libpq-dev python-dev python3-pip

RUN pip install -U pip

# Set environment variables
ENV WORK_DIR /app
ENV FLASK_APP main

# Set working directory
WORKDIR $WORK_DIR
COPY . .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port", "8080"]

EXPOSE 8080