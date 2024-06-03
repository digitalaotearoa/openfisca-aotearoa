## Setup OpenFisca Aotearoa to run in docker

## Run the application using Docker

First ensure that [Docker is installed](https://www.docker.com/get-started).

From a terminal in the root directory of the repository, build the docker image with the following command: 

```
docker build . -t openfisca-aotearoa
```

Run the image with the following command: 

```
docker run -it -v .:/openfisca -p 5000:5000 openfisca-aotearoa
```
