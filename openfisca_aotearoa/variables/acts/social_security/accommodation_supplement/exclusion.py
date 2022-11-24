"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import housing


class accommodation_supplement__social_housing_exclusion(variables.Variable):
    label = "Social housing exclusion"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        accommodation_type = people("accommodation_type", period)

        ssa2018_66 = accommodation_type == housing.AccommodationType.social_housing

        return ssa2018_66


class accommodation_supplement__other_funding_exclusion(variables.Variable):
    label = "Other funding exclusion exclusion"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        receiving_accommodation_supplement = people(
            "accommodation_supplement__receiving",
            period,
            )

        partners_accommodation_supplement = people.family.sum(
            receiving_accommodation_supplement,
            role = entities.Family.PARTNER,
            )

        ssa2018_67_a = (
            + people.has_role(entities.Family.PRINCIPAL)
            * partners_accommodation_supplement
            )

        ssa2018_67_b_i = (
            + people("student_allowance__receiving_basic_grant", period)
            + people("student_allowance__receiving_independent_circumstances", period)
        )

        ssa2018_67_b_ii = (
            + people("student_allowance__eligible_for_basic_grant", period.first_month)
            + people("student_allowance__eligible_for_independent_circumstances", period.first_month)
        )

        # TODO: ssa2018_67_b_ii
        # Would be eligible to receive one of those grants were it not for the
        # level of income of P or of P’s parent or parents or spouse or partner
        # ;or
        ssa2018_67_b_iii = (
            + people("student_allowance__would_be_eligible_for_basic_grant", period)
            + people("student_allowance__would_be_eligible_for_independent_circumstances", period)
        )

        return (
            + ssa2018_67_a
            + ssa2018_67_b_i
            + ssa2018_67_b_ii
            + ssa2018_67_b_iii
            )


class accommodation_supplement__receiving(variables.Variable):
    label = "Already receiving accommodation supplement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK
