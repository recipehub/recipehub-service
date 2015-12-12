### Recipe Microservice for RecipeHub [![Build Status](https://travis-ci.org/recipehub/recipehub-service.png)](https://travis-ci.org/recipehub/recipehub-service)

Author: [Pratik Vyas](https://github.com/pdvyas)

* Stores and versions recipes for RecipeHub
* Uses PostgresSQL JSON column type to store ingredients and steps
* Copy on Write mechanism for versioning
![Copy on write](http://i.imgur.com/4UYv2KB.png)
* Recursive querying to list versions
* Efficient forking
![Copy on write](http://i.imgur.com/tL2nlbv.png)
* Exposes a ReSTFul API

### Installation

* Clone this repository

    ```
    cd /your/projects/dir
    git clone https://github.com/recipehub/recipehub-service recipehub-service
    cd recipehub-service
    ```

* Install virtualenv, virtualenvwrapper

    ```
    sudo pip install virtualenv virtualenvwrapper
    ```

* source virtialenvwrapper.sh in your bashrc / zshrc

    ```
    echo source `which virtualenvwrapper.sh` >> ~/.bashrc
    ```

* Start a new shell or source virtualenvwrapper.sh

    ```
    source `which virtualenvwrapper.sh`
    ```

* Make a virtualenv

    ```
    mkvirtualenv recipehub-ui-dev -a `pwd` && add2virtualenv `pwd`
    ```

* Create postgres db

    ```
    createdb recipehub_service
    ```

* Install requirements

    ```
    workon recipehub-service
    pip install -r requirements.txt
    ```

### Run

    python api.py

### Test

    make test

    They are also run on Travis, https://travis-ci.org/recipehub/recipehub-service


### License

GNU GPL v3
