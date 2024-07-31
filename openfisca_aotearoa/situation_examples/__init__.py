"""This file is from the OpenFisca default country template and as such can be removed."""

import json
import os

DIR_PATH = os.path.dirname(__file__)


def parse(file_name):
    file_path = os.path.join(DIR_PATH, file_name)
    with open(file_path, "rb") as file:
        return json.loads(file.read())


child_disability_allowance = parse("child_disability_allowance.json")
