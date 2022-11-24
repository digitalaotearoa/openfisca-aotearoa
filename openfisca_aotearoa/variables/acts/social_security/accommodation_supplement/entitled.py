"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__entitled(variables.Variable):
    label = "Eligible for Accommodation Supplement"
    reference = (
        "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241",
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96264.html",
        )
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

        accommodation_type = people("accommodation_type", period)
        receives_accommodation_supplement = people("accommodation_supplement__receiving", period)
        receives_student_allowance = people("student_allowance__receiving", period)
        entitled_to_student_allowance = people("student_allowance__eligible", period)

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
        ssa2018_67_a = receives_accommodation_supplement == False
        # TODO: check if partner(s) receive
        ssa2018_67_b_i = receives_student_allowance == False
        ssa2018_67_b_ii = entitled_to_student_allowance == False
        # NOTE: (iii) says if P does not receive because of income of half the
        # planet, so we're just using previous answer for the MVP
        ssa2018_67_b_iii = entitled_to_student_allowance == False
        ssa2018_67_c = accommodation_type != housing.AccommodationType.residential_care
        # NOTE: psychiatric or intellectual handicap situation may imply:
        # 1. We collecting very sensitive personal information protected by law
        # 2. A third-party disclosing P's very sensitive personal information,
        #    in the case the aforesaid condition would render P unable to
        #    disclose such data autonomously and to non-viciously consent.
        # TODO: implement
        ssa2018_67_d = numpy.array(False)
        # (e)   P is receiving New Zealand superannuation or a veteran’s
        #       pension and the total income of P and P’s spouse or partner (if
        #       any) is more than the applicable amount specified in Part 2 of
        #       Schedule 5.
        # TODO: implement
        ssa2018_67_e = numpy.array(False)

        ssa2018_65_1_c_ii = (
            + ssa2018_67_a
            * ssa2018_67_b_i
            * ssa2018_67_b_ii
            * ssa2018_67_b_iii
            * ssa2018_67_c
            * ssa2018_67_d
            * ssa2018_67_e
            )

        return (
            + ssa2018_65_1_a
            * ssa2018_65_1_b
            * ssa2018_65_1_c_i
            * ssa2018_65_1_c_ii
            )

    def formula(persons, period, parameters):
        this_month = period.first_month

        # Based on MSD's web page
        # https://www.workandincome.govt.nz/products/a-z-benefits/accommodation-supplement.html
        age_threshold = (
            parameters(period)
            .entitlements
            .social_security
            .accommodation_supplement
            .age_threshold
            )

        # NOTE: using the age at the start of the month
        # Age changes on a DAY, but this calculation only has a granularity of MONTH
        age_requirement = persons("age", this_month.start) >= age_threshold

        # http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363772.html
        # Notwithstanding anything to the contrary in this Act or Part 6 of the Veterans’
        # Support Act 2014 or the New Zealand Superannuation and Retirement Income Act 2001,
        # the chief executive may, in the chief executive’s discretion, refuse to grant any
        # benefit or may terminate or reduce any benefit already granted or may grant a
        # benefit at a reduced rate in any case where the chief executive is satisfied
        # (a) that the applicant, or the spouse or partner of the applicant or any person
        # in respect of whom the benefit or any part of the benefit is or would be payable,
        # is not ordinarily resident in New Zealand;

        in_nz = persons(
            "social_security__ordinarily_resident_in_new_zealand",
            this_month,
            )

        resident_or_citizen = (
            + persons("immigration__resident", this_month)
            + persons("immigration__permanent_resident", this_month)
            + persons("citizenship__citizen", this_month)
            )

        social_security__accommodation_costs = persons(
            "social_security__accommodation_costs",
            this_month,
            )

        social_housing = persons("eligible_for_social_housing", this_month)
        not_social_housing = social_housing == 0

        income = persons(
            "accommodation_supplement__below_income_threshold",
            this_month,
            )

        cash = persons(
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


# Todo possibly needs renaming to social_security__eligible_for_social_housing or social_housing__eligible
class eligible_for_social_housing(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Has social housing?"
    definition_period = periods.DateUnit.MONTH
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
