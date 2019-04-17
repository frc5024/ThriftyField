docker build ./ -t thriftyfield --no-cache
docker tag thriftyfield ewpratten/thriftyfield:latest
docker push ewpratten/thriftyfield:latest