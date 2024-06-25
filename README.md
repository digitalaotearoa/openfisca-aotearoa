# OpenFisca Aotearoa

The OpenFisca Aotearoa project is an Open Source project dedicated to providing computational models of New Zealand's legislation, regulation, and government policy. 

It is a New Zealand specific Rules-as-Code project implemented in [OpenFisca](https://openfisca.org). 

> The codebase was originally started in 2018 within the "Service Innovation Lab", a New Zealand government initative that was tasked with looking at whole-of-government approaches to service innovation. The Lab was hosted within the Department of Internal Affairs (DIA) as no "whole of government" entity existed. The work included service design approaches based on life events such as the birth of a child and the idea that one service could avoid parents having to contact multiple government departments (see https://smartstart.services.govt.nz/). The Lab's eventual closure came about due to internal DIA funding priorities.

This project was continued initially by former members of the Lab and the code base, contributors and uses have widened through a number of citizen led initiatives.


## Minimal Installation - for users running the rules

This section will be available again in the near term, once a stable release strategy has been reimplemented which will see the resumption of releases on [PyPI](https://pypi.org/).

## Install Instructions for Users and Contributors

This package requires Python 3.11. These installation instructions assume python3.11 is installed and accessible via the command line [with the alias](https://www.askpython.com/python/examples/python3-alias-as-python) `python3.11`.

All platforms that can execute Python are supported, which includes GNU/Linux, macOS and Microsoft Windows.

There are a number of methodologies to setting up an development environment, the following is the most generic, other options are listed after.

### Clone the repository

Via the terminal, clone the repository and `cd openfisca-aotearoa` into the project directory.

### Setting-up a Virtual Environment with venv

In order to limit dependency conflicts, it is recommended utilising a [virtual environment](https://www.python.org/dev/peps/pep-0405/) with [venv](https://docs.python.org/3/library/venv.html).

- A [venv](https://docs.python.org/3/library/venv.html) is a project specific environment created to suit the needs of the project being worked on.

To create a virtual environment, ensuring the terminal is in the root of the openfisca-aotearoa directory (you need to have cloned this repository), then follow these instructions:

```sh
# Only required if the appropriate package is not installed (Ubuntu 22+)
sudo apt install python3.11-venv
# Create a new virtual environment in the “.venv” folder, which will contain all dependencies
python3.11 -m venv .venv 
# The following will activate the virtual environment.
source .venv/bin/activate 
```

The venv is now active and ready for installing the OpenFisca-Aotearoa dependancies.

You can deactivate that venv at any time with the following command: 

```sh
deactivate
```

(and then delete the .venv directory to completely reset the environment to restart these instructions).

### Installing the dependancies in the virtual environment

Ensuring the virtual directory is active, run the following command:

```sh
make install
```

## Testing

Ensuring the virtual directory is active and the dependancies are install in the last step run:

```sh
make test
```
This should successfully run the full OpenFisca Aotearoa test suite if everything has installed properly.

## Web API

Ensuring the virtual directory is active, to serve an instance of the OpenFisca Aotearoa web API run:

```sh
make serve
```

You can make sure that your instance of the API is working by requesting:

```sh
curl "http://localhost:5000/spec"
```

To read more about the `openfisca serve` command, check out its [documentation](https://openfisca.readthedocs.io/en/latest/openfisca_serve.html).

Depending on your environment, this will allow for access to the web API at [http://localhost:5000](http://localhost:5000).

# Alternatives

- [Run OpenFisca Aotearoa in vscode with devcontainer](docs/devcontainer.md). Creates a development environment in Visual Studio Code using the VSCode Development container approach. Requires Docker.

- [Setup your virtual environment with Pew](docs/pew.md)

- [Setup your virtual environment with pyenv](docs/pyenv.md)

- [Build a docker image and run the OpenFisca web API with it](docs/docker.md)


## Next Steps

- To write new legislation, read [the wiki](https://github.com/ServiceInnovationLab/openfisca-aotearoa/wiki) along with the OpenFisca [Coding the legislation](https://openfisca.org/doc/coding-the-legislation/index.html) section.
- To contribute to the code, read our [contribution doc](https://github.com/ServiceInnovationLab/openfisca-aotearoa/blob/master/CONTRIBUTING.md).

