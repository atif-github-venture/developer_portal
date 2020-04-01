FROM python:3.8.2-buster
RUN apt-get update -y
RUN apt-get install graphviz -y
COPY . /devportal_ui
WORKDIR /devportal_ui
RUN pip3 install --upgrade pip
RUN pip3 install --timeout 50000 -r requirements.txt
#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000 8000
ENV DEBUG=True
ENV RESTHOST="host.docker.internal:80"
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
