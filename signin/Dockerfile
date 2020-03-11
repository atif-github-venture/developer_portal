FROM python:3.8.2-buster
RUN apt-get update -y
COPY . /signin
WORKDIR /signin
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENV ENV=prod
ENTRYPOINT ["python3"]
CMD ["app.py", "run"]
