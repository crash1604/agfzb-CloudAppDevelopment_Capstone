# Car Dealership Review Platform

Welcome to the Car Dealership Review Platform repository! This project showcases a cloud-hosted web application built using Django and hosted on the IBM Cloud.

## Background

I developed this application as part of the final Capstone Project in the 10-course IBM Full Stack Cloud Developer Professional Certificate on Coursera. The initial version of the Django application was rudimentary, lacking central functionality or templates. The project's architecture and idea were provided by Coursera, with most of the design and layout predetermined. As the project was peer-reviewed against strict requirements, my focus was on implementing functionality and back-end services specified by the course instructors, rather than on improving front-end design or UX.

## Project Requirements

The goal was to build a website where users could select one of Best Car's dealerships (a fictional company) in the US to view other users' reviews of the dealership's cars and submit their own reviews. The site also included basic functionality such as a navigation bar and static "about" and "contact" pages. The website was built using the Python-Django full-stack web development framework and deployed with Red Hat Openshift/Kubernetes on the IBM Cloud.

## Architecture

![Application Architecture](link-to-image)

The dealership and review data reside in an IBM Cloudant database, while user and car data are stored in a simple SQLite database. To access data from IBM Cloudant, three IBM Cloud Functions were written, accessible through an API. Each review is analyzed by IBM Watson to determine the review's general sentiment (negative, neutral, positive).

## Setup

1. Clone the project:

