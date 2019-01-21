# IReporter Api (Challenge 3)

[![Build Status](https://travis-ci.org/PatrickMugayaJoel/Level35-C3.svg?branch=develop)](https://travis-ci.org/PatrickMugayaJoel/Level35-C3)
[![Coverage Status](https://coveralls.io/repos/github/PatrickMugayaJoel/Level35-C3/badge.svg?branch=develop)](https://coveralls.io/github/PatrickMugayaJoel/Level35-C3?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/960b6e3315c5201d1007/maintainability)](https://codeclimate.com/github/PatrickMugayaJoel/Level35-C3/maintainability)

IReporter is a government system that enables citizens to bring any form of corruption to the notice of appropriate authorities and the general public.
Users can also report on things that needs government intervention
    

## Getting Started

Clone this github repository:  `$ https://github.com/PatrickMugayaJoel/Andela-35.git`

## Prerequisites

* A text editor e.g. Sublime Text, Notepad++, Visual Studio Code
* A web browser e.g. Google Chrome, Mozilla Firefox

## Features

* User can signup.
* User can report a red flag).
* User can view all Red flag.
* User can update a Red flag
 
## Languages

* PYTHON 3.7
 
## Installing

* Install python 3.7
* Clone [this repository](https://github.com/PatrickMugayaJoel/Andela-35/tree/develop) to your local computer.
* Setup a virtual enviroment and activate it
* Install requirements
* Execute the 'run.py' file in the root directory.

## Basic Endpoints

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /ireporter/api/v2/users | User Signup|
| POST | /ireporter/api/v2/login | User login|
| POST | /ireporter/api/v2/red-flags | Adding a Red_flag |
| GET | /ireporter/api/v2/red-flags | list Red flag |
| GET | /ireporter/api/v2/red-flags/1 | Get Red flag with id 1 |
| PUT | /ireporter/api/v2/red-flags/1 | Update a Red flag |
| GET | /ireporter/api/v2/users | List Users |
| POST | /ireporter/api/v2/red-flags/1/comments | Add a comment |
| GET | /ireporter/api/v2/red-flags/1/comments | View comments |
| UPDATE | /ireporter/api/v2/comments/1 | update a comment |
| DELETE | /ireporter/api/v2/comments/1 | delete a comment |


## Authors

* **Mugaya Joel Patrick** (josean.patrick11@gmail.com)
 
## Acknowledgments

* Andela

