"""Formula for establishing eligibility for the OSCAR subsidy and the possibly hours payable for said subsidy."""

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


class oscar_subsidy__granted(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = False
    label = "Are payments under the oscar subsidy granted for this child"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96299"  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s21"  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282529"  # 2004
        ]
