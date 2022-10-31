docker run --name postgres -e POSTGRES_PASSWORD=postgres -d -p 5432:5432  --mount type=bind,source=$(realpath tests),target=/app postgres
