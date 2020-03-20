#Docker build script
cd devportal_flaskapi <br/>
docker image rm -f devportal_flaskapi <br/>
docker build -t devportal_flaskapi . <br/>
docker run -p 80:80 -it devportal_flaskapi <br/>
docker ps <br/>

** to override, but wont work with test/dev on docker
docker run -e "env=prod" -p 80:80 -it devportal_flaskapi

#To run from CLI
ENV=prod python3 app.py run


https://www.datacamp.com/community/tutorials/web-development-django
https://medium.com/@himanshuxd/how-to-create-registration-login-webapp-with-django-2-0-fd33dc7a6c67
https://github.com/overiq/TGDB/tree/e5c32aeb89da5a2214a63c34df793db91ad65197/django_project/blog
https://overiq.com/django-1-10/django-rendering-fields-manually/