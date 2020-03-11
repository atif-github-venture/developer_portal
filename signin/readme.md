#Docker build script
cd navtest <br/>
docker image rm -f signin <br/>
docker build -t signin . <br/>
docker run -p 8080:8080 -it signin <br/>
docker ps <br/>

#To run from CLI
ENV=prod python3 app.py run
