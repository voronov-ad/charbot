FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY parse-company.py .
ENTRYPOINT ["python3"]
CMD ["parse-company.py"]
#CMD [ "python3", "-m" , "parse-company", "run", "--host=0.0.0.0"]