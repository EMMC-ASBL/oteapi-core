# Open Translation Environment API 


## Run in Docker
### Development target
The development target will allow for automatic reloading when source code changes. This requires that the local directory is bind-mounted using the -v or --volume argument. To Build and run the development target from the command line:

	
	docker build --rm -q -f Dockerfile \
	  --label "ontotrans.oteapi=development" \
	  --target development \
	  -t "ontotrans/oteapi-development:latest" .
	
	
### Production target
The production target will not reload itself on code change and will run a predictable version of the code on port 80. Also you might want to use a named container with the --restart=always option to ensure that the container is restarted indefinately regardless of the exit status. To build and run the production target from the command line:

	
	docker build --rm -q -f Dockerfile \
	  --label "ontotrans.oteapi=production" \	  
	  -t "ontotrans/oteapi:latest" .
	
	
### Run redis
Redis with persistance needs to run as a prerequisite to starting oteapi. Redis needs to share the same network as oteapi

	
    docker network create -d bridge otenet
	docker volume create redis-persist
	docker run \
		--detach \
		--name redis \
		--volume redis-persist:/data \
		--network otenet \
		redis:latest
	

### Run oteapi (development)
Run the services by attaching to the otenet network and set the environmental variables for connecting to Redis.
	
	docker run \
		--rm \
		--network otenet \
		--detach \
  		--volume ${PWD}:/app \
  		--publish 8080:8080 \
  		--env REDIS_TYPE=redis \
  		--env REDIS_HOST=redis \
  		--env REDIS_PORT=6379 \
  		ontotrans/oteapi-development:latest

Open the following url in a browser [http://localhost:8080/redoc](http://localhost:8080/redoc)

### Run the Atmoz SFTP Server
To test the data access via SFTP, the atmoz sftp-server can be run

	
	docker volume create sftpdrive
	docker run \
		--detach \
		--network=otenet \
		--volume sftpdrive:/home/foo/upload \
		--publish 2222:22 \
		 atmoz/sftp foo:pass:1001
	
