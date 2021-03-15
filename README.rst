
# Keep secrets out of source control

$ cp .env.example .env
$ cp .sftp_conf_example.json .sftp_conf.json

$ docker-compose up -d

Activate local environment
$ pytest