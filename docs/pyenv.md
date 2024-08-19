## Setup Aotearoa OpenFisca with pyenv

This approach with pyenv due to the nature of pyenv does not require python to be installed to get started.

### Step 1: Clone the repo

Clone this repository and then in a terminal ensure you are in it's root directory
```sh
cd openfisca-aotearoa
```

### Step 2: Install pyenv

Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

Add to `.bashrc` or `.zshrc`:

```sh
eval "$(pyenv init -)"
if which pyenv-virtualenv-init >/dev/null; then eval "$(pyenv virtualenv-init -)"; fi
```

And then run:

```sh
pyenv install 3.11.9
pyenv virtualenv 3.11.9 openfisca-aotearoa-3.11.9
pyenv local openfisca-aotearoa-3.11.9
python --version # This should match the version in .python-version file
```

### Step 3: Install dev dependencies

```sh
make install
```

:tada: OpenFisca Aotearoa Package is now installed and ready, refer to the `README.md` for instructions on how to run tests or serve the web API.
