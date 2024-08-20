"""Variables representative of definitions defined in the Social Security Regulations."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class social_security_regulation__household_income(variables.Variable):
    value_type = float
    entity = entities.Family
    definition_period = periods.WEEK
    label = "The sum of total income of a childs caregiver and their spouse or partner"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96282",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s20-p1-d9",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282509",  # 2004
        "https://www.workandincome.govt.nz/map/income-support/extra-help/childcare-assistance-programme/income-test-01.html"  # MSD Interpretation, note they reference income test 1 rather than household income
        ]
