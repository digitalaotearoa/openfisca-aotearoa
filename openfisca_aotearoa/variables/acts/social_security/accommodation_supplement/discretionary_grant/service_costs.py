"""Accommodation supplement's service costs.

Service costs are those determined by MSD of any services provided to or in
connection with the premises, excluding the cost of water supply.

"""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__service_costs(variables.Variable):
    label = "Accommodation supplement's service costs"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783242"
    documentation = """
        Service costs are those determined by MSD of any services provided to
        or in connection with the premises, excluding the cost of water supply.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        # (2) In this subpart, unless the context otherwise requires,— [...]
        # service costs, in relation to any premises,—

        #     (a) means the cost as reasonably determined by MSD of any
        #         services (for example, electricity supply, gas supply,
        #         telephone network connection, or broadband Internet
        #         connection) provided to or in connection with the premises
        #         for consumption or use by the occupants of the premises; but
        ssa2018_part_2_sub_10_65_2_a = people(
            "social_security__service_costs",
            period,
            )

        #     (b) does not include the cost of water supplied to the premises.
        ssa2018_part_2_sub_10_65_2_b = people(
            "accommodation_supplement__water_supply", period,
            )

        total_costs = (
            + ssa2018_part_2_sub_10_65_2_a
            - ssa2018_part_2_sub_10_65_2_b
            )

        return numpy.maximum(total_costs, 0)


class accommodation_supplement__water_supply(variables.Variable):
    label = "Accommodation supplement's water supply costs"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783242.html"
    documentation = """Cost of water supplied to the premises."""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK
