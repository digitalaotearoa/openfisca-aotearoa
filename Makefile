all: lint test

uninstall:
	pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

install:
	@# Install OpenFisca-Aotearoa for development.
	@# `make install` installs the editable version of OpenFisca-Aotearoa.
	@# This allows contributors to test as they code.
	pip install --upgrade pip
	poetry install --sync

check-syntax-errors:
	python -m compileall -q .

format:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	poetry run isort `git ls-files | grep "\.py$$"`
	poetry run autopep8 `git ls-files | grep "\.py$$"`
	poetry run pyupgrade --py39-plus `git ls-files | grep "\.py$$"`

lint: clean check-syntax-errors format
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	poetry run flake8 `git ls-files | grep "\.py$$"`
	poetry run pylint `git ls-files | grep "\.py$$"`
	poetry run yamllint `git ls-files | grep "\.yaml$$"`

test: clean check-syntax-errors
ifdef yaml
	openfisca test -c openfisca_aotearoa openfisca_aotearoa/tests/$(yaml)
else
	openfisca test --country-package openfisca_aotearoa openfisca_aotearoa/tests
endif

serve:
	openfisca serve --country-package openfisca_aotearoa -b 0.0.0.0:5000 --reload
