FROM python:3.8.2-buster
RUN apt-get update -y
COPY . /devportal_api
WORKDIR /devportal_api
RUN pip3 install --upgrade pip
RUN pip3 install --timeout 50000 -r requirements.txt
EXPOSE 80 80
ENV ENV=prod
ENTRYPOINT ["python3"]
CMD ["manage.py", "run"]
