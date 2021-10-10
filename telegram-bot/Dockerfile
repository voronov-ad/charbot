FROM python:3.8-slim-buster
RUN mkdir app
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["bot.py"]
