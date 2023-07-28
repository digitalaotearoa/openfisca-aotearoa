"""Exegesis — Housing costs.

Housing costs are the on-going costs of rent, board, lodging, or ownership.

"""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class housing_costs(variables.Variable):
    label = "Exegesis — Housing costs"
    reference = "https://www.workandincome.govt.nz/housing/live-in-home/housing-costs/index.html"
    documentation = """On-going costs of rent, board, lodging, or ownership."""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula(people, period, _params):
        tenants = people("residential_tenancies__tenant", period)
        rent = people.premise("residential_tenancies__rent", period)
        bond = people.premise("residential_tenancies__bond", period)

        return (rent + bond) * tenants / numpy.add.reduce(tenants)
