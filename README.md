# devops-assignments

This repository contains an example spring boot application which needs to be built and deployed to a kubernetes cluster.

## Repository structure

The repository contains three folders in its root:

- application: the spring boot application
- assignments: contains assignments for you to solve
- kubernetes: contains python scripts to deploy and destroy a kubernetes cluster in digitalocean. 

*Attention:* You do not have to spin up a kubernetes cluster. We already have one setup for you - see the [Get your kubeconfig file](#kubeconfig)

## Preparation

### Setup accounts

You need the following accounts for the assignments.

- github account: To fork this repository
- dockerhub account: To build and push the docker image of the demo application

### Install software

You need the following software installed on your machine to complete the assignments.

- docker: You need docker installed and running to build the application.
- kubectl: You need kubectl installed to access the kubernetes cluster and deploy the application.
- make: The application can be built with a makefile (optional, you can also use mvn directly).

### <a name="kubeconfig"></a>Get your kubeconfig file

We prepared a kubernetes cluster for the assignment.

Please send [us](mailto://cloud+devopsassignment@foryouandyourcustomers.com) your public gpg key to. We will use the gpg key to encrypt the kubeconfig and send it to you.

### Fork the repository

Create a [fork](https://guides.github.com/activities/forking/) of this repository.

You can commit your code and notes into your fork - this makes sharing your results easy and convenient.

### Update settings.xml (in your fork!)

The settings.xml file is used by maven to configure the dockerhub credentials and the image name and tag.

Copy the file [`application/.m2/settings.xml.example`](./application/.m2/settings.xml.example) to `application/.m2/settings.xml` and fill in your dockerhub information.

## Assignments

With the git repository forked, the settings.xml ready and the kubeconfig in place you can start working on the assignments.

We tried to order the assignments by their complexity. Have a look at the [assignments](./assignments) folder.
