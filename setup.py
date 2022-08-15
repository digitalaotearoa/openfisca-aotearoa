"""This file contains OpenFisca-Aotearoa package's metadata and dependencies."""

from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()  # pylint: disable=W1514

setup(
    name = "OpenFisca-Aotearoa",
    version = "12.1.0",
    author = "New Zealand Government, Service Innovation Lab",
    author_email = "brenda.wallace@dia.govt.nz,hamish.fraser@dia.govt.nz",
    description = "OpenFisca tax and benefit system for Aotearoa",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = "benefit microsimulation social tax",
    license = "http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/ServiceInnovationLab/openfisca-aotearoa",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [
        (
            "share/openfisca/openFisca-aotearoa",
            ["CHANGELOG.md", "README.md"],
            ),
        ],
    install_requires = [
        "openfisca-core[web-api] @ git+https://github.com/openfisca/openfisca-core.git@add-weeks",
        ],
    extras_require = {
        "dev": [
            "autopep8 >= 1.5.4, < 2.0.0",
            "flake8 >= 3.8.0, < 4.0.0",
            "flake8-bugbear >= 20.1.0, < 22.0.0",
            "flake8-builtins >= 1.5.0, < 2.0.0",
            "flake8-coding >= 1.3.0, < 2.0.0",
            "flake8-commas >= 2.0.0, < 3.0.0",
            "flake8-comprehensions >= 3.2.0, < 4.0.0",
            "flake8-docstrings >= 1.5.0, < 2.0.0",
            "flake8-import-order >= 0.18.0, < 1.0.0",
            "flake8-print >= 3.1.0, < 5.0.0",
            "flake8-quotes >= 3.2.0, < 4.0.0",
            "flake8-simplify >= 0.9.0, < 1.0.0",
            "flake8-use-fstring >= 1.1.0, < 2.0.0",
            "pylint >= 2.6.0, < 3.0.0",
            "pycodestyle >= 2.6.0, < 3.0.0",
            "pyupgrade >= 2.32.0, < 3.0.0",
            ],
        },
    packages = find_packages(),
    )
