
# Keep secrets out of source control

$ cp .env.example .env
$ cp .sftp_conf_example.json .sftp_conf.json

# Build and test the 

docker-compose -f docker-compose.yml -f docker-compose-dev.yml build
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d
docker-compose exec ontoapi pytest