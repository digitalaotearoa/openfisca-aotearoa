## Setup Aotearoa OpenFisca

### Step 1: Clone the repo

```sh
git clone https://github.com/ServiceInnovationLab/openfisca-aotearoa.git
cd openfisca-aotearoa
```

### Step 2: Install Python

Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

And then add to `.bashrc` or `.zshrc`:

```sh
eval "$(pyenv init -)"
if which pyenv-virtualenv-init >/dev/null; then eval "$(pyenv virtualenv-init -)"; fi
```

And then run:

```sh
pyenv install 3.10.4
pyenv virtualenv openfisca-aotearoa-3.10.4
pyenv local openfisca-aotearoa-3.10.4
python --version # This should match the version in .python-version file
```

### Step 3: Install dev dependencies

```sh
pip install --upgrade pip build twine
pip install --use-deprecated=legacy-resolver --upgrade --editable ".[dev]"
```

:tada: This OpenFisca Country Package is now installed and ready!

### Step 4: Running the tests

```sh
make test
```

> [Learn more about tests](https://openfisca.org/doc/coding-the-legislation/writing_yaml_tests.html)

:tada: This OpenFisca Aotearoa Package is now installed and ready!

## Serve OpenFisca Aotearoa with the OpenFisca Web API

If you are considering building a web application, you can use the packaged OpenFisca Web API.

To serve the Openfisca Web API locally, run:

```sh
openfisca serve --port 5000
```

To read more about the `openfisca serve` command, check out its [documentation](https://openfisca.readthedocs.io/en/latest/openfisca_serve.html).

You can make sure that your instance of the API is working by requesting:

```sh
curl "http://localhost:5000/spec"
```

This endpoint returns the [Open API specification](https://www.openapis.org/) of your API.

:tada: OpenFisca Aotearoa is now served by the OpenFisca Web API! To learn more, go to the [OpenFisca Web API documentation](https://openfisca.org/doc/openfisca-web-api/index.html)
