# Conwell's Game of Life 
The pupose of this project is to demostrate my technical ability in development and operations. 

This application was quite fun to build, and decided to expand on the scope even though he specification for the game was to only build an STDOUT shell script.

This code could have written in simple __main__ type manner,  but I wish to demostrate my abilites in Testing, OOP, Systems Design, API Development, HTML and Ochestration. For this reason I wrote out a full scope with proper development and production environments. 

I thank you in advance for your consideration and hope that the resuts meet your acceptance criteria. 

# Customer Requirements 

# DevOps Requirments

Constuct load balanced web service/app that prints the Host Name & IP addres of the server the traffic is being load balanced to. 

The service should be deployed to VPS in on AWS EC2, which each host being deployed on a linux instance. 

IAM user credential should be provided to the completed environement for assesment. 

# Conwell's Game Of Life 

Develop a simple version of Conwell's game of life. The should random generate cell, the user should be able to specify the grid size and number of generations to run through. 

# Solution 

The solution for both requirements are written in Python and Django and deployed to the same applicationf or ease of use, and features the following:

1. WebApp for viewing Host name and IP addres
2. The WebApp also shows a wokring exmample of conwell's Game
3. And API for querying host details 
4. An django management command for running Conwell's Game of life on the shell
5. A fully working Docker container for running the solution locally 

# Design Principles 

Below are some of the design principles I've followed in the developlemt of this solution.

## Domain Driven Design 
This method tries to have the structure of the Code and Services model the language of the Domain Experts. The function names & classes closely matches human readable language, and map to the bussines rules. I do this by establishing a ubiquitous language between domain experts and technical execution. 

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

The name of the function above closely matches the bussines rules it executes, writting code in this style has a number of advantages: 

1. Its easy for stakeholders to understand the follow of the system and provide usefull feedback
2. Code closely matches the expected outcome, there is less ambiguity 
3. The code is self documenting 

# TDD/BDD

I am strong advocate for test driven development, I always plan my work out 1st and write the test before I write a single line of code. 

This coupled with DDD and Uqiquites language ensure that my code written to explicitly satisify real user requirements. 

I use a combindation of dataproviders to map out scenarios, and the built python unit tests run my regression packs.

Under normal circumstances I would have build Gherkin style test to define my success creteria, this is also usefull for stakeholders so they can understand my intentions Unfortunately there was not enough time in this assesemnt, but examples of how I go about doing this can be found here ()

# SOLID Principle

The practice of SOLID is important to writting code that can scale complexity, Single Responsbility is the most important aspect for this test. 

It was very easy to combine certain condition such under or overpuplation, and it would have been wrong to do so. But for the sake of this excercise I seperated those functions to seperate concerns to show my general approach to designing code. 

Writting code in this manner makes following the Agile methodology significantly easire. My code is broken down into the smallest possible work packets, so they can be acurately sized with a predical shipping strategy. And, because its written in a dependancies 1st style, value of features can be shipped/delivered incremently and tested and signed of in issolation, making for for safe delpoys and higher qualitfy of code. 

# REST API 

The app is also accompanied with an REST API built using django-rest-framework, I did include auth for the purpose of this excercise. That would require a database wich would have increased the complexity of the load-balanced server deployment. But in the real world I would always start with athenctication (see this application) 

# Ochestration 

The dev enviroment was using docker-compose, and can easily be deploy to a local environemnt if you have docker-desktop. Instructions will follow below. 

The production environemtn is deploy using EC2 instances with VPS (IAM user credential to be supplied) 

# Instructions 

The Web Application Be found Here 
http://18.135.173.194/









