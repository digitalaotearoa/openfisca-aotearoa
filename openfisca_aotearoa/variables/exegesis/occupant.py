"""Occupant.

An occupant is a person who occupies a premise.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class occupant(variables.Variable):
    label = "Exegesis — Occupant"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """A person who occupies a premise."""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula(people, _period, _params):
        return (
            + people.has_role(entities.Premise.APPLICANT)
            + people.has_role(entities.Premise.OCCUPANT)
            )
