FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY vacancy_parser.py .
ENTRYPOINT ["python3"]
CMD ["vacancy_parser.py"]