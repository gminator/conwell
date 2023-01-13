# Conwell's Game of Life 
The purpose of this project is to demonstrate my technical ability in development and operations. 

This application was quite fun to build, and I decided to expand on the scope even though the specification for the game was to only build a simple STDOUT shell script and basic hosting environment.

This code could have  been written in a  simple __main__ type manner,  but I wish to demonstrate my abilities  in Testing, OOP, Systems Design, API Development, HTML and Orchestration. For this reason I wrote out a full scope with proper design principles, development and production environments. 

I thank you in advance for your consideration and hope that the results meet your acceptance criteria. 

# Customer Requirements 

This assessment  has 2 basic requirements  outlined below. 

### DevOps Requirements

Construct a load balanced web service/app that prints the Host Name & IP address of the server the traffic is being load balanced to. 

The service should be deployed to a VPS in on AWS EC2, with which each host being deployed on a Linux instance. 

IAM user credential should be provided to the completed environment for assessment. 

### Conwell's Game Of Life 

Develop a simple version of Conwell's game of life. The should randomly generate live cells and the user should be able to specify the grid size and number of generations to run through. 

# Solution 

The solution for both requirements are written in Python and Django and deployed to the same application for ease of use, and features the following:

1. WebApp for viewing Host name and IP address
2. The WebApp also shows a working example of Conwell’s Game
3. And API for querying host details 
4. A Django management command for running Conwell's Game of life as  a shell script
5. A fully working Docker container for running the solution locally 

# Design Principles 

Below are some of the design principles I've followed in the development of this solution.

### Domain Driven Design 
This methodology tries to have the structure of the Code and Services to model the language of the Domain Experts. The function names & classes closely matches human readable language, and map to the business rules. I do this by establishing a ubiquitous language between domain experts and technical execution, I facilitate this through workshops, flow diagrams, wireframes and documentation. 

For example. 

```python
def under_populated(self,):
		"""
		Under Populated
		Any live cell with fewer than two live neighbours dies, as if by underpopulation.
		- Return
		boolean True|False
		"""
		return len(self.living_neighbors()) < 2 and self.is_alive()
```

The name of the function above closely matches the business rules it executes, writing code in this style has a number of advantages: 

1. It’s easy for stakeholders & developers to understand the flow of the system and provide useful feedback
2. Code closely matches the expected outcome, there is less ambiguity 
3. The code is self-documenting 

### TDD/BDD

I am strong advocate for test driven development, I always plan my work out 1st and write the test before I write a single line of code. 

This coupled with DDD and Ubiquities language ensure that my is code written to explicitly satisfy real user requirements. 

I use a combination of data providers to map out scenarios, and the built in python unit tests run my regression packs.

Under normal circumstances I would have built Gherkin style user stores to define my success criteria, this is also useful for stakeholders so they can understand my intentions. Unfortunately there was not enough time in this assessment, but examples of how I go about doing this can be found here (Poker Game)

### SOLID Principle

The practice of SOLID is important to writing code that can scale complexity, Single Responsibility is the most important aspect for this test. 

It was very easy to combine certain condition such under or overpopulation, and it would have been wrong to do so. But for the sake of this exercise I structured those functions to separate concerns to show my general approach to designing code. 

Writing code in this manner makes following the Agile methodology significantly easier. My code is broken down into the smallest possible work packets, so they can be accurately sized with a predicable shipping strategy. And, because its written in a dependencies 1st style, value of features can be shipped/delivered inclemently and tested and signed of in isolation, making for for safe deploys and higher quality of code. 

### REST API 

The app is also accompanied with an REST API built using django-rest-framework, I did include auth for the purpose of this exercise. That would require a database which would have increased the complexity of the load-balanced server deployment. But in the real world I would always start with authentication (see this application) 

### Orchestration 

The dev environment was using docker-compose, and can easily be deploy to a local environment if you have docker-desktop. Instructions will follow below. 

The production environment is deploy using EC2 instances with VPS (IAM user credential to be supplied) 

# Instructions 

Instructions for the various results can be found below. 

### Web Application 
There is basic web application, built using Ngnix load balancer, Django and bootstrap 5. 

The page will output the node rendering the content, a JavaScript example of the game and some other links of interest 

http://18.135.173.194/


### REST API 

There is also a very simple example of the a REST API that returns the node details. 

A sample curl request can be found bellow.

```bash

curl --location --request POST 'http://18.135.173.194/api/'

```

### Django STDOUT 

There is also Django management command from which the game can be execute 

# Docker Installation Instruction 


The app is easily install & configured using Docker, all packages and configurations will automatically be deployed. 

It will configure the following: 
1. Django3 + Django Rest Framework + Python3
2. Postgress Service 

Follow the instructions below to run the service.

### Step 1: Install Docker Desktop 

Follow the instructions for your Operating System, if you don't already have Docker Desktop

[Docker Desktop - Mac](https://docs.docker.com/desktop/install/mac-install/)

[Docker Desktop - Windows](https://docs.docker.com/desktop/install/windows/)

[Docker Desktop - Ubuntu](https://docs.docker.com/desktop/install/ubuntu/)


### Step 2: Clone & Configure Container 

Once docker is installed you may clone and configure the container.

```sh=
#Clone & Start Docker Container
git clone git@github.com:gminator/conwell.git
cd conwell
docker-compose up -d
```

### Step 3: Run Unit Tests
```sh=
docker exec -it conwell python manage.py test
```


# Special Notes 

Below are additional things I might have done given more time. 

1. Written out a full set of User Stories for each feature
2. Configure the EC2 instances using orchestration tools like Ansible or Chef
3. Deployed Cloudflare Infront the load balancer for CDN & SSL certs 
4. Made the WebApp responsive or mobile friendly 
5. Deployed shared MySQL or Postgress Database for Authentication 
6. Written the README to more closely resemble the documentation I provide my engineers before embarking on a project









![image](https://user-images.githubusercontent.com/724922/212318845-4aa314ff-c88e-402c-ae8e-22fd9ecd0adb.png)
