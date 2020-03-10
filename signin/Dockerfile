FROM python:3.8.0
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /signin
WORKDIR /signin
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
