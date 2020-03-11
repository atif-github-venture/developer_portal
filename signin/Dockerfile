FROM python:3.8.0
RUN apt-get update -y
COPY . /signin
WORKDIR /signin
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["ENV=prod", "python3", "app.py", "run"]
