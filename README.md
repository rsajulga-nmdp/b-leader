# HLA-B Leader Peptide Microservice and Tool

The HLA-B Leader Assessment Tool (BLEAT) was developed, described, and validated by Sajulga et al., 2021 (*submitted for publication*) (*1*). BLEAT automates leader matching, as discovered by <a target="_blank" href="https://doi.org/10.1016/S2352-3026(19)30208-X" tabindex="-1">Petersdorf et al., 2020</a> (*2*).

1. R. Sajulga, Y. Bolon, M. Maiers, E. W. Petersdorf, Assessment of *HLA-B* Genetic Variation with an HLA-B Leader Tool and Implications in Clinical Transplantation.
2. E. W. Petersdorf, M. Carrington, C. O'HUigin, M. Bengtsson, D. De Santis, V. Dubois, T. Gooley, M. Horowitz, K. Hsu, J. A. Madrigal, M. J. Maiers, M. Malkki, C. McKallor, Y. Morishima, M. Oudshoorn, S. R. Spellman, J. Villard, P. Stevenson, T. International Histocompatibility Working Group in Hematopoietic Cell, <a target="_blank" href="https://doi.org/10.1016/S2352-3026(19)30208-X" tabindex="-1">Role of HLA-B exon 1 in graft-versus-host disease after unrelated haemopoietic cell transplantation: a retrospective cohort study</a>. *Lancet Haematol* **7**, e50-e60 (2020).

This tool classifies the leader peptides (either M or T at position -21) and matching statuses of HLA-B alleles and ranks them based on outcome measures.

# Table of Contents
- [Instructions](#instructions-)
- [Background](#background-)
- [Setup](#setup-)
    - [B-Leader REST Service](#b-leader-rest-service-)
        - [Web Service Bootstrapping](#web-service-bootstrapping-)
        - [Web Service Initialization](#web-service-initialization-)
        - [Testing](#testing-)
    - [B-Leader Web Application](#b-leader-web-application-)
        - [Web App Boostrapping](#web-app-bootstrapping-)
        - [Web App Initialization](#web-app-initialization-)
    - [B-Leader Rest End Points Docker Container](#b-leader-rest-end-points-docker-container-)
        - [Prerequisite](#prerequisite-)
        - [Docker image build](#docker-image-build-)
        - [Docker container launch](#docker-container-launch-)
        - [Stopping the running container](#stopping-the-running-container-)
    - [B-Leader Web Application Docker Container](#b-leader-web-application-docker-container-)
        - [Webapp Docker Prerequisite](#webapp-docker-prerequisite-)
        - [Webapp Docker image build](#webapp-docker-image-build-)
        - [Webapp Docker container launch](#webapp-docker-container-launch-)
        - [Stopping the running webapp container](#stopping-the-running-webapp-container-)
    - [B-Leader Deployment With Docker Compose](#b-leader-deployment-with-docker-compose-)
        - [Deployment Prerequisite](#deployment-prerequisite-)
        - [App Deployment](#app-deployment-)
        - [App Undeploy](#app-undeploy-)
- [B-Leader Production Deployment](#b-leader-production-deployment-)
    - [Unified Container Deployment](#unified-container-deployment-)
    - [Decoupled Containers Deployment](#decoupled-containers-deployment-)

## Instructions [⤴](#table-of-contents)
Instruction for using the REST endpoints can be found [here](https://github.com/nmdp-bioinformatics/b-leader/wiki/REST-Endpoints).

An example demonstration for using the REST service on a trimmed HLA dataset is available in the [example](example/README.md) folder.

## Background [⤴](#table-of-contents)
- [HLA](https://github.com/nmdp-bioinformatics/b-leader/wiki/HLA-Background)
- [HLA-B Leader Peptides](https://github.com/nmdp-bioinformatics/b-leader/wiki/HLA%E2%80%90B-Leader-RESTful-Microservice-and-Tool)

# Setup [⤴](#table-of-contents)

## B-Leader REST Service [⤴](#table-of-contents)

### Web Service Bootstrapping [⤴](#table-of-contents)

To begin, ensure that you have Python3 installed. To check, issue this command to verify your python version:
```
python --version
```

If Python3 is not installed, please download it from [here](https://www.python.org/downloads/).

If Python3 is readily available, set up your virtual environment by running these commands:
```
python3 -m venv venv
source venv/bin/activate
```

Pip is the package installer for Python. It comes pre-packaged with Python. This will be used to install our requirements as such:
```
pip install --upgrade pip
pip install -r requirements.txt
```

Once installed, *behave* will be available for testing and *Flask* will be available to set up the web service.

### Web Service Initialization [⤴](#table-of-contents)

Initialize the web service via this command:
```
python server.py
```

Once initialized, you may use the REST API endpoints at http://0.0.0.0:5010/. Usage is detailed [here](https://github.com/nmdp-bioinformatics/b-leader/wiki/REST-Endpoints)

> *REST → **Re**presentational **S**tate **T**ransfer*
 *API → **A**pplication **P**rogramming **I**nterface*


### Testing [⤴](#table-of-contents)

##### BDD Testing [⤴](#table-of-contents)

This repository was developed through *Behavior-Driven Development (BDD)*.
Running all the BDD tests in this repository is as simple as running this command:
```
behave
```

##### BDD Results Report [⤴](#table-of-contents)
The results of your BDD tests can sometimes be difficult to view in the terminal. To view the tests results in the browser, we can use *allure-behave*, which was installed by pip during the [bootstrapping process](#bootstrapping-).

You will first need to specify *behave* to generate formatted *allure* results

```
behave -f allure_behave.formatter:AllureFormatter -o tests/results/
```

Finally, to view these formatted results in the browser, enter this command:
```
allure serve tests/results
```

## B-Leader Web Application [⤴](#table-of-contents)

This front-end graphical user interface (GUI) was created using Angular 8.

#### Web app bootstrapping [⤴](#table-of-contents)

We will need to go into the web app project's root folder
```
cd webapp
```

Since our web application uses JavaScript (Angular 8), install Node.js (≥10.9) and npm (node package manager) [here](https://nodejs.org/en/download/) if ```npm``` is not a recognized command in your terminal.

Through npm, we can install our dependencies by running:
```
npm install
```

#### Web app initialization [⤴](#table-of-contents)

Once finished, ensure that the back-end REST server has been initialized on http://0.0.0.0:5010/ as detailed [here](#web-service-initialization-).

And then run a local development server:
```
ng serve
```

The web application will now be available on https://0.0.0.0:4200/.

## B-Leader Rest End Points Docker Container [⤴](#table-of-contents)

### Prerequisite [⤴](#table-of-contents)
The containerization is facilitated by [Docker Container](https://www.docker.com/resources/what-container). 

To be able to run Docker container, a docker set up and configuration is necessary. The installation details can be found in the [official docker documentation](https://docs.docker.com/get-docker/).

### Docker image build [⤴](#table-of-contents)
To build the image, navigate to the directory where `Dockerfile-flask` is located
Execute the comand (keep an eye on required "." at the end of the command)
```
docker build -t nmdpbioinformatics/b-leader-backend:latest -f Dockerfile-flask .
```
Now the image should be built and available in the local docker registry

### Docker container launch [⤴](#table-of-contents)
To start a container form docker image (built in the last step) we need to execute the following command

```
docker run -d -p 5010:5010 nmdpbioinformatics/b-leader-backend:latest
```
Upon successful execution a container id should comeout. We can see the container if it is up by executing
```
docker ps -a
```
That should show us if the container is up and running. If it is up then we should be able to navigate to http://localhost:5010/ to see the API landing page.

### Stopping the running container [⤴](#table-of-contents)
We have to obtain the container id by executing 
```
docker ps -a
```
Then we have to execute 
```
docker stop $CONTAINER_ID
```

## B-Leader Web Application Docker Container [⤴](#table-of-contents)

### Webapp Docker Prerequisite [⤴](#table-of-contents)

[B-Leader Rest End Points Docker Container](#b-leader-rest-end-points-docker-container-) is up and runninng for the webapp container to be working properly (for build that is not necessary).

The containerization is facilitated by [Docker Container](https://www.docker.com/resources/what-container). 

To be able to run Docker container, a docker set up and configuration is necessary. The installation details can be found in the [official docker documentation](https://docs.docker.com/get-docker/).

### Webapp Docker image build [⤴](#table-of-contents)
To build the image, navigate to the `webapp` directory where `Dockerfile` is located.
We will need to go into the web app project's root folder using the following command
```
cd webapp
```
Execute the command below(keep an eye on required "." at the end of the command)
```
docker build --build-arg CONFIGURATION="" -t nmdpbioinformatics/b-leader-ui-app .
```
Now the image should be built and available in the local docker registry.

### Webapp Docker container launch [⤴](#table-of-contents)
To start the webapp container form docker image (built in the last step) we need to execute the following command

```
docker run -d -p 80:80 -t nmdpbioinformatics/b-leader-ui-app:latest
```
Upon successful execution a container id should comeout. We can see the container if it is up by executing by executing
```
docker ps -a
```
That should show us if the container is up and running. If it is up then we should be able to navigate to http://localhost:80/ to see the Web App landing page.

### Stopping the running webapp container [⤴](#table-of-contents)
We have to obtain the container id by executing 
```
docker ps -a
```
Then we have to execute 
```
docker stop $CONTAINER_ID
```

## B-Leader Deployment With Docker Compose [⤴](#table-of-contents)
**Warning: This segment is designed for local development purpose, seperate `docker-compose` file configuration is needed be developed for production deployment with docker-compose.**
The app front end and back end both can be deployed using [Docker Compose](https://docs.docker.com/compose/).

### Deployment Prerequisite [⤴](#table-of-contents)
[Docker Compose](https://docs.docker.com/compose/) have to be installed and docker registry have to contain the images a) `be-the-match/b-leader-ui-app` and b) `be-the-match/b-leader-backend`.

### App Deployment [⤴](#table-of-contents)
Simply execute the following command where `docker-compose.yml` file is located to deploy the application frontend and backend
```
docker-compose up -d
```

### App Undeploy [⤴](#table-of-contents)
To undeploy the app simply execute the following command where `docker-compose.yml` file is located
```
docker-compose down
```

## B-Leader Production Deployment [⤴](#table-of-contents)
The production deployment has two model, a) unified container model and b) segregated contaienrs model. 

a) The unified container packes both the backend (python-flask-gunicorn) and front end (angular and nginx) into one docker docker images while during the runtime Nginx acts as an webserver for front end and reverse proxy for backend. 

b) The segregated container deployment would provide independent scalling of backend and front end cluster should there be any need for it. Although the decoupling might be desireable under certain circumstances but this feature would require setting up an approprite network using docker compose or Kubernetes and are currently not available.

### Unified Container Deployment [⤴](#table-of-contents)
The production `apiUrl` should be adjusted with correct server in the file `webapp/src/environments/environment.prod.ts`

To build the docker image the following command may be executed in the project root directory:
```
docker build --build-arg CONFIGURATION="production" -t nmdpbioinformatics/b-leader .
```
After successful build we should have the docker image available in our local docker registry.

To deploy the app now we can use the following command. The application should be available in your domain, i.e. `http://host:80/`
```
docker run -d -p 80:80 -t nmdpbioinformatics/b-leader:latest
```
To stop the app container, We have to obtain the container id by executing 
```
docker ps -a
```
Then we have to execute 
```
docker stop $CONTAINER_ID
```

### Decoupled Containers Deployment [⤴](#table-of-contents)
This feature is under development now.