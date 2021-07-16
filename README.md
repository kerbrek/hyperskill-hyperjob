# HyperJob Agency

Implementation of the [HyperJob Agency project](https://hyperskill.org/projects/94) (Django) from [JetBrains Academy](https://www.jetbrains.com/academy/).

## Branches

* [azure-app-service](https://github.com/kerbrek/hyperskill-hyperjob/tree/azure-app-service) - project configured for deployment to Azure App Service (available at https://www.hyperjob.ml/)
* [compose](https://github.com/kerbrek/hyperskill-hyperjob/tree/compose) - project configured as a containerized Compose application

## Prerequisites

* pipenv
* make

## Commands

* Setup a virtual environment using _Pipenv_

    `make install`

* Start a development Web server

    `make run`

* Run tests

    `make test`

* Run linter

    `make lint`

* List all available _Make_ commands

    `make help`
