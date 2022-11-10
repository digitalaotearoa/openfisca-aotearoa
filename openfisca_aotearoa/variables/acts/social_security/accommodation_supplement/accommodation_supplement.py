"""TODO: Add missing doctring."""

from pathlib import Path
import string

import numpy
import pandas

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import housing


# TODO: Review against the new 2018 act
class accommodation_supplement__eligible(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Eligible for Accommodation Supplement"

    reference = """
        61DH Purpose of accommodation supplement

        The purpose of sections 61E to 61EC and Schedule 18 is to provide targeted
        financial assistance to help certain people with high accommodation costs
        to meet those costs.
        """

    def formula(persons, period, parameters):
        # Based on MSD's web page
        # https://www.workandincome.govt.nz/products/a-z-benefits/accommodation-supplement.html
        age_threshold = parameters(
            period).entitlements.social_security.accommodation_supplement.age_threshold
        # NOTE: using the age at the start of the month
        # Age changes on a DAY, but this calculation only has a granularity of MONTH
        age_requirement = persons("age", period.start) >= age_threshold

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
            "social_security__ordinarily_resident_in_new_zealand", period)
        resident_or_citizen = persons("immigration__resident", period) + persons(
            "immigration__permanent_resident", period) + persons("citizenship__citizen", period)
        social_security__accomodation_costs = persons(
            "social_security__accomodation_costs", period)
        not_social_housing = (
            persons("eligible_for_social_housing", period) == 0)

        income = persons(
            "accommodation_supplement__below_income_threshold", period)
        cash = persons(
            "accommodation_supplement__below_cash_threshold", period)

        return age_requirement * resident_or_citizen * in_nz * social_security__accomodation_costs * not_social_housing * income * cash


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


class accommodation_supplement__base(variables.Variable):
    label = "Social Security Regulations 2018 §17 Base rate"
    reference = "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96264.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        # (2) The base rate is as follows:
        #
        # Beneficiaries who are single

        # We assume beneficiary of jobseeker support.
        beneficiaries = people("social_security__beneficiary", period)
        rate = people("jobseeker_support__base", period)

        # We assume single as in "no partner"
        mingled = people("social_security__in_a_relationship", period)
        singles = numpy.logical_not(mingled)

        # We calculate the number of dependent children.
        f_members = people.family.members
        dependent = sum(f_members("social_security__dependent_child", period))
        children = dependent >= 1
        no_child = numpy.logical_not(children)

        # (a) for a single beneficiary under the age of 25 years, the maximum
        #     weekly rate of a benefit that the beneficiary would have been
        #     entitled to receive, before any abatement or deduction, if the
        #     beneficiary had attained the age of 25 years:

        # We assume age on Monday
        monday = period.first_day

        # We assume under 25 years by Monday
        age = people("age", monday)
        under25y = age < 25

        # We need to create a new simulation to calculate a benefit, where
        # people would be 25 years by Monday this week. We assume jobseeker.
        #
        # 1. We clone the current simulation:
        simulation = people.simulation.clone()

        # 2. We delete the actual result of jobseeker base rate:
        simulation.delete_arrays("jobseeker_support__base", period)

        # 3. We make everybody 25 years old:
        simulation.delete_arrays("age", monday)
        simulation.set_input("age", monday, numpy.repeat(25, len(people.ids)))

        # 4. Finally, we delete the result of any other variable we need to
        # recalculate (in our case those related to single beneficiaries):
        for letter in string.ascii_lowercase[0:6]:
            simulation.delete_arrays(f"schedule_4__part1_1_{letter}", period)

        # 5. Then, we recalculate jobseeker base rate as if having 25 years:
        base25y = simulation.calculate("jobseeker_support__base", period)

        # 6. After, we restore the original ages:
        simulation.delete_arrays("age", monday)
        simulation.set_input("age", monday, age)       

        # 7. And we re-invalidate the cached calculations:
        for letter in string.ascii_lowercase[0:6]:
            simulation.delete_arrays(f"schedule_4__part1_1_{letter}", period)

        # And apply all the conditions.
        ssr17_2_a = singles * beneficiaries * no_child * under25y * base25y

        # (b) for a single beneficiary with 1 or more dependent children,—
        #     (i)   the maximum weekly rate of a benefit that the beneficiary
        #           is entitled to receive, before any abatement or deduction;
        #           plus
        #     (ii)  the maximum annual rate of family tax credit (divided by
        #           52) that is payable in respect of an eldest dependent child
        #           who is under 16 years old under subparts MA to MF and MZ of
        #           the Income Tax Act 2007:

        # We calculate the maximum amount of tax credit for the eldest.
        this_year = period.this_year
        tax_credit = people("family_tax_credit__eldest", this_year, "add") / 52


        # And apply all the conditions.
        ssr17_2_b = singles * beneficiaries * children * (rate + tax_credit)

        # (c) for any other single beneficiary, the maximum weekly rate of a
        #     benefit that the beneficiary would be entitled to receive before
        #     any abatement or deduction:

        # We get the reminder of the beneficiaries.
        leastwise25y = numpy.logical_not(under25y)

        # And apply all the conditions.
        ssr17_2_c = singles * beneficiaries * no_child * leastwise25y * rate

        return ssr17_2_a + ssr17_2_b + ssr17_2_c


class AccommodationSupplement__Situation(indexed_enums.Enum):
    unknown = "We have no idea"
    situation_1 = "Situation 1"
    situation_2 = "Situation 2"
    situation_3 = "Situation 3"
    situation_4 = "Situation 4"
    situation_5 = "Situation 5"
    situation_6 = "Situation 6"


class accommodation_supplement__situation(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = entities.Person
    value_type = indexed_enums.Enum
    possible_values = AccommodationSupplement__Situation
    default_value = AccommodationSupplement__Situation.unknown
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        families = people.family
        family_members = families.members("social_security__dependent_child", period)
        dependent_children = sum(family_members)
        partners = families.nb_persons(entities.Family.PARTNER)
        accommodation_type = people("accommodation_type", period)

        rent_board_lodging = (
            + (accommodation_type == housing.AccommodationType.rent)
            + (accommodation_type == housing.AccommodationType.board)
            + (accommodation_type == housing.AccommodationType.lodging)
            )

        mortgage = accommodation_type == housing.AccommodationType.mortgage

        ssa_sched_4_part_7_1 = (
            + (
                + (dependent_children >= 1) * (partners >= 1)
                + (dependent_children >= 2) * (partners == 0)
                )
            * rent_board_lodging
            * AccommodationSupplement__Situation.situation_1.index
            )

        ssa_sched_4_part_7_2 = (
            + (
                + (dependent_children == 0) * (partners >= 1)
                + (dependent_children == 1) * (partners == 0)
                )
            * rent_board_lodging
            * AccommodationSupplement__Situation.situation_2.index
            )

        ssa_sched_4_part_7_3 = (
            + numpy.logical_not(ssa_sched_4_part_7_1)
            * numpy.logical_not(ssa_sched_4_part_7_2)
            * rent_board_lodging
            * AccommodationSupplement__Situation.situation_3.index
            )

        ssa_sched_4_part_7_4 = (
            + (
                + (dependent_children >= 1) * (partners >= 1)
                + (dependent_children >= 2) * (partners == 0)
                )
            * mortgage
            * AccommodationSupplement__Situation.situation_4.index
            )        

        ssa_sched_4_part_7_5 = (
            + (
                + (dependent_children == 0) * (partners >= 1)
                + (dependent_children == 1) * (partners == 0)
                )
            * mortgage
            * AccommodationSupplement__Situation.situation_5.index
            )        


        ssa_sched_4_part_7_6 = (
            + numpy.logical_not(ssa_sched_4_part_7_4)
            * numpy.logical_not(ssa_sched_4_part_7_5)
            * mortgage
            * AccommodationSupplement__Situation.situation_6.index
            )

        return (
            + ssa_sched_4_part_7_1
            + ssa_sched_4_part_7_2
            + ssa_sched_4_part_7_3
            + ssa_sched_4_part_7_4
            + ssa_sched_4_part_7_5
            + ssa_sched_4_part_7_6
            + AccommodationSupplement__Situation.unknown.index
            )


class accommodation_supplement__rebate(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        last_week = period.last_week
        situation = people("accommodation_supplement__situation", last_week)
        accommodation_costs = people("accommodation_costs", last_week)
        rebate = params(period).acts.social_security.accommodation_supplement.rebate
        base_rate = people("accommodation_supplement__base", last_week)

        ssa_sched_4_part_7_1 = (
            + (situation == AccommodationSupplement__Situation.situation_1)
            * (
                + accommodation_costs
                - (
                    + rebate["section_1"]["accommodation_costs"]
                    * (accommodation_costs - rebate["section_1"]["base_rate"] * base_rate)
                    )
                )
            )

        ssa_sched_4_part_7_2 = (
            + (situation == AccommodationSupplement__Situation.situation_2)
            * (
                + accommodation_costs
                - (
                    + rebate["section_2"]["accommodation_costs"]
                    * (accommodation_costs - rebate["section_2"]["base_rate"] * base_rate)
                    )
                )
            )

        ssa_sched_4_part_7_3 = (
            + (situation == AccommodationSupplement__Situation.situation_3)
            * (
                + accommodation_costs
                - (
                    + rebate["section_3"]["accommodation_costs"]
                    * (accommodation_costs - rebate["section_3"]["base_rate"] * base_rate)
                    )
                )
            )

        ssa_sched_4_part_7_4 = (
            + (situation == AccommodationSupplement__Situation.situation_4)
            * (
                + accommodation_costs
                - (
                    + rebate["section_4"]["accommodation_costs"]
                    * (accommodation_costs - rebate["section_4"]["base_rate"] * base_rate)
                    )
                )
            )

        ssa_sched_4_part_7_5 = (
            + (situation == AccommodationSupplement__Situation.situation_5)
            * (
                + accommodation_costs
                - (
                    + rebate["section_5"]["accommodation_costs"]
                    * (accommodation_costs - rebate["section_5"]["base_rate"] * base_rate)
                    )
                )
            )

        ssa_sched_4_part_7_6 = (
            + (situation == AccommodationSupplement__Situation.situation_6)
            * (
                + accommodation_costs
                - (
                    + rebate["section_6"]["accommodation_costs"]
                    * (accommodation_costs - rebate["section_6"]["base_rate"] * base_rate)
                    )
                )
            )

        return (
            + ssa_sched_4_part_7_1
            + ssa_sched_4_part_7_2
            + ssa_sched_4_part_7_3
            + ssa_sched_4_part_7_4
            + ssa_sched_4_part_7_5
            + ssa_sched_4_part_7_6
            )


class accommodation_supplement__part_of_nz(variables.Variable):
    label = "TODO"
    reference = "https://datafinder.stats.govt.nz/layer/27780-urban-area-2017-generalised-version/"
    documentation = """TODO"""
    entity = entities.Person
    value_type = str
    default_value = "Other"
    definition_period = periods.DateUnit.WEEK


class AccommodationSupplement__AreaOfResidence(indexed_enums.Enum):
    unknown = "We have no idea"
    area_1 = "Area 1"
    area_2 = "Area 2"
    area_3 = "Area 3"
    area_4 = "Area 4"


class accommodation_supplement__area_of_residence(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = entities.Person
    value_type = indexed_enums.Enum
    possible_values = AccommodationSupplement__AreaOfResidence
    default_value = AccommodationSupplement__AreaOfResidence.unknown
    definition_period = periods.DateUnit.WEEK

    def formula(people, period, _params):
        params_path = "openfisca_aotearoa/parameters"
        file_path = "acts/social_security/accommodation_supplement"
        area_path = Path(f"{params_path}/{file_path}/area.csv").resolve()
        last_week = period.last_week
        part_of_nz = people("accommodation_supplement__part_of_nz", last_week)
        area_of_nz = pandas.read_csv(area_path, sep = ";")

        parts_of_residence = (
            numpy.flatnonzero(area_of_nz["UA2017_NAME"].isin([part_of_nz]))
            for part_of_nz in part_of_nz
            )

        areas_of_residence = (
            AccommodationSupplement__AreaOfResidence[area_of_nz.at[index[0], "SSA2018_AREA"]].index
            if len(index) > 0
            else AccommodationSupplement__AreaOfResidence.area_4.index
            for index in parts_of_residence
            )

        return numpy.fromiter(areas_of_residence, dtype = int)


class accommodation_supplement__cutout(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        last_week = period.last_week
        situation = people("accommodation_supplement__situation", last_week)
        area_of_residence = people("accommodation_supplement__area_of_residence", last_week)
        cutout = params(period).acts.social_security.accommodation_supplement.cutout

        ssa_sched_4_part_7_1 = (
            + (situation == AccommodationSupplement__Situation.situation_1)
            * cutout["section_1"][area_of_residence]
            )

        ssa_sched_4_part_7_2 = (
            + (situation == AccommodationSupplement__Situation.situation_2)
            * cutout["section_2"][area_of_residence]
            )

        ssa_sched_4_part_7_3 = (
            + (situation == AccommodationSupplement__Situation.situation_3)
            * cutout["section_3"][area_of_residence]
            )

        ssa_sched_4_part_7_4 = (
            + (situation == AccommodationSupplement__Situation.situation_4)
            * cutout["section_4"][area_of_residence]
            )

        ssa_sched_4_part_7_5 = (
            + (situation == AccommodationSupplement__Situation.situation_5)
            * cutout["section_5"][area_of_residence]
            )

        ssa_sched_4_part_7_6 = (
            + (situation == AccommodationSupplement__Situation.situation_6)
            * cutout["section_6"][area_of_residence]
            )

        return (
            + ssa_sched_4_part_7_1
            + ssa_sched_4_part_7_2
            + ssa_sched_4_part_7_3
            + ssa_sched_4_part_7_4
            + ssa_sched_4_part_7_5
            + ssa_sched_4_part_7_6
            )
