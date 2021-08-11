oteapi
======

Build
-----

Local environment variable setup

    cp .env.example .env
    cp .sftp_conf_example.json .sftp_conf.json

Modify your .env .sftp_conf.json and keep them out of source control.


Build and run

    docker-compose build
    docker-compose up


Testing
-------

    docker-compose exec ontoapi pytest
