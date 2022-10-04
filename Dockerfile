FROM python:3.9

WORKDIR /code
COPY requirements.txt requirements.txt
COPY templates templates
COPY main.py main.py

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]
