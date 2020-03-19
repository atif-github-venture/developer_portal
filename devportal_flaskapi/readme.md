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