all: lint test

uninstall:
	pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip build twine setuptools

install: deps
	@# Install OpenFisca-Aotearoa for development.
	@# `make install` installs the editable version of OpenFisca-Aotearoa.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade

build: clean deps
	@# Install OpenFisca-Extension-Template for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-Extension-Template, the same we put in the hands of users and reusers.
	python -m build
	find dist -name "*.whl" -exec pip install --force-reinstall {}[dev] \;

check-syntax-errors:
	python -m compileall -q .

format:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	isort `git ls-files | grep "\.py$$"`
	autopep8 `git ls-files | grep "\.py$$"`
	pyupgrade --py39-plus `git ls-files | grep "\.py$$"`

lint: clean check-syntax-errors format
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`
	pylint `git ls-files | grep "\.py$$"`
	yamllint `git ls-files | grep "\.yaml$$"`

test: clean check-syntax-errors
	ifdef yaml
		openfisca test -c openfisca_aotearoa openfisca_aotearoa/tests/$(yaml)
	else
		openfisca test --country-package openfisca_aotearoa openfisca_aotearoa/tests
	endif

serve: build
	openfisca serve --country-package openfisca_aotearoa -b 0.0.0.0:5000 --reload
