# Quiz
## Demo video
https://drive.google.com/file/d/1mX6ds17MT2Z-q11JPuJvGlHQTyCCKF41/view?usp=drivesdk
## Requirements

* Docker Compose 1.21.2+
* Python 3.6 +

## Run with Docker Compose

```bash
# building the container
sudo docker-compose build

# starting up a container
sudo docker-compose up
```

## Build the virtual environment

```bash
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install -r test-requirements.txt
```

## Swagger definition

```http
http://localhost:8081/v1/swagger.json
```

## Health Check

```http
http://localhost:8081/v1/ping
```

## Launch tests
