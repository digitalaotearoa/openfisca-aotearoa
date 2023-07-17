"""Social security's service costs.

Service costs as defined for accommodation supplement and youth support
payment.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class social_security__service_costs(variables.Variable):
    label = "Social security's service costs"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784375.html"
    documentation = """
        Service costs as defined for accommodation supplement and youth support
        payment.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        # service costs—

        # (a) is defined in section 65 for the purposes of subpart 10 of Part 2
        #     and Part 7 of Schedule 4 (accommodation supplement); and
        ssa2018_schedule_2_service_costs_a = people(
            "accommodation_supplement__service_costs",
            period,
            )

        # (b) is defined in section 162 (obligations of young person granted
        #     youth support payment) for the purposes of that section
        ssa2018_schedule_2_service_costs_b = people(
            "youth_payment__service_costs",
            period,
            )

        return (
            + ssa2018_schedule_2_service_costs_a
            + ssa2018_schedule_2_service_costs_b
            )
