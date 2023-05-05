# DataScience.HackDay.FaceDetector

#### To run locally
- install required dependencies: `pip install -r requirements.txt`
- run app: `uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload`

#### To build docker container and push to azure
##### Prerequisite
- Install Docker for Windows
- create Azure Container Registry using Azure Portal
- configure docker cli: `az acr login --name <azure container registry name>`
##### Steps
- build docker container: `docker build --platform x86_64 -t mugshot-detector .`
- tag & push to container registry: `docker tag mugshot-detector <azure container registry name>.azurecr.io/mugshot-detector` and then `docker push <azure container registry name>.azurecr.io/mugshot-detector`
