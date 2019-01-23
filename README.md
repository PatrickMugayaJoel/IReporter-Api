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
* User can report a red flag.
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

| REQUEST TYPE | ROUTE | PUBLIC ACCESS | FUNCTIONALITY |
| ------------- | ----- | ------------- | ------------- |
| POST | /ireporter/api/v2/users | TRUE | User Signup|
| POST | /ireporter/api/v2/login | TRUE | User login|
| POST | /ireporter/api/v2/red-flags | FALSE | Adding a Red_flag |
| GET | /ireporter/api/v2/red-flags | TRUE | list Red flag |
| GET | /ireporter/api/v2/red-flags/1 | TRUE | Get Red flag with id 1 |
| PUT | /ireporter/api/v2/red-flags/1 | FALSE | Update a Red flag |
| GET | /ireporter/api/v2/users | FALSE | List Users |
| UPDATE | /ireporter/api/v2/comments/1 | FALSE | update a comment |


## Authors

* **Mugaya Joel Patrick** (josean.patrick11@gmail.com)
 
## Acknowledgments

* Andela

