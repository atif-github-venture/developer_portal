#Docker build script
cd user <br/>
docker image rm -f user <br/>
docker build -t user . <br/>
docker run -p 80:80 -it user <br/>
docker ps <br/>

** to override, but wont work with test/dev on docker
docker run -e "env=prod" -p 80:80 -it user

#To run from CLI
ENV=prod python3 app.py run
