"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.acts.social_security.accommodation_supplement.situation import (
    AccommodationSupplement__Situation,
    )
from openfisca_aotearoa.variables.demographics.housing import AccommodationType


class accommodation_supplement__rebate(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        situation = people("accommodation_supplement__situation", period)
        accommodation_costs = people("accommodation_costs", period)
        accommodation_type = people("accommodation_type", period)
        base_rate = people("accommodation_supplement__base", period)

        rebate = (
            params(period)
            .social_security
            .accommodation_supplement
            .rebate
            )

        situations = [
            situation == member
            for member in tuple(AccommodationSupplement__Situation)[1:]
            ]

        # TODO: move to parameter
        rate = (accommodation_type == AccommodationType.lodging) * .62 + 1

        ssa2018_sched_4_part_7_1_to_6 = [
            + accommodation_costs * rate
            - rebate[f"section_{i}"]["accommodation_costs"]
            * (
                + accommodation_costs * rate
                - rebate[f"section_{i}"]["base_rate"] * base_rate
                )
            for i in range(1, 7)
            ]

        return numpy.select(situations, ssa2018_sched_4_part_7_1_to_6)
