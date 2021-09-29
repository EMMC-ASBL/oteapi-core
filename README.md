# FastAPI/Python Service Template

This is a template for building modular web services with a
best-practise organization of files using the FastAPI web framework.

## Run in Docker
### Development target
The development target will allow for automatic reloading when source code changes. This requires that the local directory is bind-mounted using the -v or --volume argument. To Build and run the development target from the command line:


	docker build --rm -q -f Dockerfile \
	  --label "ontotrans.fastservice-target=development" \
	  --target development \
	  -t "ontotrans/fastservice-development:latest" .

	docker run --rm -i --user="$(id -u):$(id -g)" -p 8080:8080 -v "$PWD:/app" ontotrans/fastservice-development:latest

Open http://localhost:8080 on your browser to test the application.

### Production target
The production target will not reload itself on code change and will run a predictable version of the code on port 80. Also you might want to use a named container with the --restart=always option to ensure that the container is restarted indefinately regardless of the exit status. To build and run the production target from the command line:


	docker build --rm -q -f Dockerfile \
	  --label "ontotrans.fastservice-target=production" \
	  --target production \
	  -t "ontotrans/fastservice-production:latest" .

	docker run -d -p 80:80 --user="$(id -u):$(id -g)" --name fastservice --restart=always ontotrans/fastservice-production:latest


docker run -it --network=scinet \
  -v $PWD:/app \
  -p 8000:8080 \
  -e REDIS_TYPE=redis \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  dlite-oteapi


## Run the Atmoz SFTP Server
docker run --network=scinet -v /home/thomas/Documents/atmoz/pub:/home/foo/upload \
    -p 2222:22 -d atmoz/sftp \
    foo:pass:1001



## Example
	1. Create a session
		curl -X 'POST' \
		'http://localhost:8000/api/v1/session/' \
		-H 'accept: application/json' \
		-H 'Content-Type: application/json' \
		-d '{
		"label":"testing"
		}'

		received session-id: 86e90705-ab20-4052-8b2f-2b1cb07bef87

	2. Create a datasource
		curl -X 'POST' \
		'http://localhost:8000/api/v1/datasource/' \
		-H 'accept: application/json' \
		-H 'Content-Type: application/json' \
		-d '{
		"downloadUrl": "https://www.iphonehuset.no/files/simple-close-reflection-600.jpg",
		"mediaType": "image/jpg",
		"configuration": {}
		}'

	3.