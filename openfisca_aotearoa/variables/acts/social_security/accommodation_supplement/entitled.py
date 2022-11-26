"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__entitled(variables.Variable):
    label = "Eligible for Accommodation Supplement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        accommodation_costs = people(
            "accommodation_supplement__accommodation_costs",
            period,
            )

        assets_requirement = people(
            "accommodation_supplement__assets_requirement",
            period,
            )

        social_housing_exclusion = people(
            "accommodation_supplement__social_housing_exclusion",
            period,
            )

        other_funding_exclusion = people(
            "accommodation_supplement__other_funding_exclusion",
            period,
            )

        # 65    Accommodation supplement: discretionary grant
        # (1)   MSD may grant a person (P), for the period that MSD determines
        #       an accommodation supplement if—
        #       (a) P has accommodation costs; and
        ssa2018_65_1_a = accommodation_costs

        #       (b) P meets the assets requirement (as set out in regulations
        #           made under section 423); and
        ssa2018_65_1_b = assets_requirement

        #       (c) P is not excluded on either of the following grounds:
        #           (i)     the social housing exclusion:
        ssa2018_65_1_c_i = numpy.logical_not(social_housing_exclusion)

        #           (ii)    the other funding exclusion.
        ssa2018_65_1_c_ii = numpy.logical_not(other_funding_exclusion)

        return (
            + ssa2018_65_1_a
            * ssa2018_65_1_b
            * ssa2018_65_1_c_i
            * ssa2018_65_1_c_ii
            )

    def formula_1964_12_04(people, period, params):
        this_month = period.first_month

        # Based on MSD's web page
        # https://www.workandincome.govt.nz/products/a-z-benefits/accommodation-supplement.html
        age_threshold = (
            params(period)
            .social_security
            .accommodation_supplement
            .age_threshold
            )

        # NOTE: using the age at the start of the month
        # Age changes on a DAY, but this calculation only has a granularity of MONTH
        age_requirement = people("age", period.first_day) >= age_threshold

        # http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363772.html
        # Notwithstanding anything to the contrary in this Act or Part 6 of the Veterans’
        # Support Act 2014 or the New Zealand Superannuation and Retirement Income Act 2001,
        # the chief executive may, in the chief executive’s discretion, refuse to grant any
        # benefit or may terminate or reduce any benefit already granted or may grant a
        # benefit at a reduced rate in any case where the chief executive is satisfied
        # (a) that the applicant, or the spouse or partner of the applicant or any person
        # in respect of whom the benefit or any part of the benefit is or would be payable,
        # is not ordinarily resident in New Zealand;

        in_nz = people(
            "social_security__ordinarily_resident_in_new_zealand",
            this_month,
            )

        resident_or_citizen = (
            + people("immigration__resident", this_month)
            + people("immigration__permanent_resident", this_month)
            + people("citizenship__citizen", this_month)
            )

        social_security__accommodation_costs = people(
            "social_security__accommodation_costs",
            this_month,
            )

        social_housing = people("social_housing__eligible", period)
        not_social_housing = social_housing == 0

        income = people(
            "accommodation_supplement__below_income_threshold",
            this_month,
            )

        cash = people(
            "accommodation_supplement__below_cash_threshold",
            this_month,
            )

        return (
            + age_requirement
            * resident_or_citizen
            * in_nz
            * social_security__accommodation_costs
            * not_social_housing
            * income
            * cash
            )


# Todo possibly needs renaming to social_security__social_housing__eligible or social_housing__eligible
class social_housing__eligible(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Has social housing?"
    definition_period = periods.DateUnit.WEEK
    reference = "Social Security Act 1964 - 61EA Accommodation supplement http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM362856"


class accommodation_supplement__below_income_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Income is below Accommodation Supplement threshold?"
    definition_period = periods.DateUnit.MONTH


class accommodation_supplement__below_cash_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Cash is below Accommodation Supplement threshold?"
    definition_period = periods.DateUnit.MONTH
