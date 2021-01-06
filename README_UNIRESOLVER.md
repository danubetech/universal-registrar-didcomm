To build and run a docker image for the uniresolver service:

```
docker build . -f docker/Dockerfile.did_resolution_server -t universalresolver/didcomm:latest
docker-compose up
```
