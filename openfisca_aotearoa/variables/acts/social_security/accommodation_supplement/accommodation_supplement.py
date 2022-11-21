"""TODO: Add missing doctring."""

from pathlib import Path
import string

import numpy
import pandas

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import housing


class accommodation_supplement__entitled(variables.Variable):
    label = "Eligible for Accommodation Supplement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        accommodation_costs = people("accommodation_costs", period)

        return accommodation_costs > 0

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
        members = families.members("social_security__dependent_child", period)
        dependent_children = sum(members)
        partners = families.nb_persons(entities.Family.PARTNER)
        accommodation_type = people("accommodation_type", period)

        # As conditions 1-3 and 4-6 differ only in the accommodation type, we
        # first calculate the "base condition" (w/o accommodation type).
        cond_1 = (
            + (dependent_children >= 1) * (partners >= 1)
            + (dependent_children >= 2) * (partners == 0)
            )
        cond_2 = (
            + (dependent_children == 0) * (partners >= 1)
            + (dependent_children == 1) * (partners == 0)
            )
        cond_3 = (
            + numpy.logical_not(cond_1)
            * numpy.logical_not(cond_2)
            )

        # Then we calculate conditions 1-3.
        rent_board_lodge = (
            + (accommodation_type == housing.AccommodationType.rent)
            + (accommodation_type == housing.AccommodationType.board)
            + (accommodation_type == housing.AccommodationType.lodging)
            )
        ssa_sched_4_part_7_1_to_3 = (cond_1, cond_2, cond_3) * rent_board_lodge

        # And conditions 4-6.
        mortgage = accommodation_type == housing.AccommodationType.mortgage
        ssa_sched_4_part_7_4_to_6 = (cond_1, cond_2, cond_3) * mortgage
        
        # Finally we create a list of conditions and situations.
        conditions = *ssa_sched_4_part_7_1_to_3, *ssa_sched_4_part_7_4_to_6
        situations = tuple(AccommodationSupplement__Situation)[1:]
        fallback = AccommodationSupplement__Situation.unknown

        # And we return the situations corresponding to the conditions.
        return numpy.select(conditions,  situations, fallback)


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
        base_rate = people("accommodation_supplement__base", period)

        rebate = (
            params(period)
            .acts
            .social_security
            .accommodation_supplement
            .rebate
            )

        situations = [
            situation == member 
            for member in tuple(AccommodationSupplement__Situation)[1:]
            ]

        ssa_sched_4_part_7_1_to_6 = [
            + accommodation_costs
            - rebate[f"section_{i}"]["accommodation_costs"]
            * (
                + accommodation_costs 
                - rebate[f"section_{i}"]["base_rate"] * base_rate
                )
            for i in range(1, 7)
        ]

        return numpy.select(situations, ssa_sched_4_part_7_1_to_6)


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
        area_of_residence = AccommodationSupplement__AreaOfResidence
        params_path = "openfisca_aotearoa/parameters"
        file_path = "acts/social_security/accommodation_supplement"
        area_path = Path(f"{params_path}/{file_path}/area.csv").resolve()

        # We read locations from a database.
        part_of_nz = people("accommodation_supplement__part_of_nz", period)
        area_of_nz = pandas.read_csv(area_path, sep = ";")
        name = area_of_nz["UA2017_NAME"]
        area = "SSA2018_AREA"
        locations = (numpy.flatnonzero(name.isin([loc])) for loc in part_of_nz)
        
        # The we map locations to each area 1-4.
        areas_of_residence = (
            area_of_residence[area_of_nz.at[index[0], area]].index 
            if len(index) > 0 else area_of_residence.area_4.index 
            for index in locations
            )

        # And return the result.
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
        situation = people("accommodation_supplement__situation", period)
        area = people("accommodation_supplement__area_of_residence", period)

        cutout = (
            params(period)
            .acts
            .social_security
            .accommodation_supplement
            .cutout
            )

        situations = [
            situation == member 
            for member in tuple(AccommodationSupplement__Situation)[1:]
            ]


        ssa_sched_4_part_7_1_to_6 = [
            cutout[f"section_{i}"][area] 
            for i in range(1, 7)
            ]

        return numpy.select(situations, ssa_sched_4_part_7_1_to_6)
