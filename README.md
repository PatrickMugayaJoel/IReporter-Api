# IReporter Api (Challenge 3)

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

## Endpoints

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /ireporter/api/v2/users | User Signup|
| POST | /ireporter/api/v2/red-flags | Report a Red flag |
| GET | /ireporter/api/v2/red-flags | list Red flag |
| GET | /ireporter/api/v2/red-flags/1 | Get Red flag with id 1 |
| PATCH | /ireporter/api/v2/red-flags/1 | Update a Red flag |
| GET | /ireporter/api/v2/users | List Users |


## Authors

* **Mugaya Joel Patrick** (josean.patrick11@gmail.com)
 
## Acknowledgments

* Andela

