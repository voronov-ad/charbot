FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY vacancy-parser.py .
ENTRYPOINT ["python3"]
CMD ["employee-parser.py"]
#CMD [ "python3", "-m" , "parse-company", "run", "--host=0.0.0.0"]