FROM ubuntu:22.04

RUN apt-get update

RUN apt install -y python-is-python3

WORKDIR /site

RUN apt-get install -y python3-pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]