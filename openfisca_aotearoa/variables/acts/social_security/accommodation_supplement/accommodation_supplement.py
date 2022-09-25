"""TODO: Add missing doctring."""

from pathlib import Path

import numpy
import pandas

from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import DateUnit
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Family, Person


# TODO: Review against the new 2018 act
class accommodation_supplement__eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = DateUnit.MONTH
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
class eligible_for_social_housing(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = "Has social housing?"
    definition_period = DateUnit.MONTH
    reference = "Social Security Act 1964 - 61EA Accommodation supplement http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM362856"


class accommodation_supplement__below_income_threshold(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = "Income is below Accommodation Supplement threshold?"
    definition_period = DateUnit.MONTH


class accommodation_supplement__below_cash_threshold(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = "Cash is below Accommodation Supplement threshold?"
    definition_period = DateUnit.MONTH


class accommodation_supplement__base(Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.WEEK


class AccommodationSupplement__Situation(Enum):
    unknown = """
        We have no idea
        """
    situation_1 = """
        To a person who has 1 or more dependent children and who is in a
        relationship, or a sole parent with 2 or more dependent children,
        whose accommodation costs are rent or payments for board and lodgings
        """
    situation_2 = """
        To a person who has no dependent children and who is in a relationship,
        or a sole parent with 1 dependent child, whose accommodation costs are
        rent or payments for board and lodgings
        """
    situation_3 = """
        To any other person whose accommodation costs are rent or payments for
        board and lodgings
        """
    situation_4 = """
        To a person who has 1 or more dependent children and who is in a
        relationship, or a sole parent with 2 or more dependent children, whose
        accommodation costs are the sum of payments required under any mortgage
        security, and other payments that the chief executive is satisfied are
        reasonably required to be made in respect of the person’s home
        """
    situation_5 = """
        To a person who has no dependent children and who is in a relationship,
        or a sole parent with 1 dependent child, whose accommodation costs are
        the sum of payments required under any mortgage security, and other
        payments that the chief executive is satisfied are reasonably required
        to be made in respect of the person’s home
        """
    situation_6 = """
        To any other person whose accommodation costs are the sum of payments
        required under any mortgage security, and other payments that the chief
        executive is satisfied are reasonably required to be made in respect of
        the person’s home
        """


class accommodation_supplement__situation(Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = Person
    value_type = Enum
    possible_values = AccommodationSupplement__Situation
    default_value = AccommodationSupplement__Situation.unknown
    definition_period = DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        families = people.family
        last_week = period.last_week
        family_members = families.members("social_security__dependent_child", last_week)
        dependent_children = sum(family_members)
        partners = families.nb_persons(Family.PARTNER)

        ssa_sched_4_part_7_1 = (
            + (
                + (dependent_children >= 1) * (partners >= 1)
                + (dependent_children >= 2) * (partners == 0)
                )
            * AccommodationSupplement__Situation.situation_1.index
            )

        ssa_sched_4_part_7_2 = (
            + (
                + (dependent_children == 0) * (partners >= 1)
                + (dependent_children == 1) * (partners == 0)
                )
            * AccommodationSupplement__Situation.situation_2.index
            )

        ssa_sched_4_part_7_3 = False  # TODO: Add "for board and rent"
        ssa_sched_4_part_7_4 = False  # TODO: Add "for sum of mortgage"
        ssa_sched_4_part_7_5 = False  # TODO: Add "for sum of mortgage"
        ssa_sched_4_part_7_6 = False  # TODO: Add "for sum of mortgage"

        return (
            + ssa_sched_4_part_7_1
            + ssa_sched_4_part_7_2
            + ssa_sched_4_part_7_3
            + ssa_sched_4_part_7_4
            + ssa_sched_4_part_7_5
            + ssa_sched_4_part_7_6
            + AccommodationSupplement__Situation.unknown.index
            )


class accommodation_supplement__rebate(Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.WEEK

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


class accommodation_supplement__part_of_nz(Variable):
    label = "TODO"
    reference = "https://datafinder.stats.govt.nz/layer/27780-urban-area-2017-generalised-version/"
    documentation = """TODO"""
    entity = Person
    value_type = str
    default_value = "Other"
    definition_period = DateUnit.WEEK


class AccommodationSupplement__AreaOfResidence(Enum):
    unknown = "We have no idea"
    area_1 = "Area 1"
    area_2 = "Area 2"
    area_3 = "Area 3"
    area_4 = "Area 4"


class accommodation_supplement__area_of_residence(Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = Person
    value_type = Enum
    possible_values = AccommodationSupplement__AreaOfResidence
    default_value = AccommodationSupplement__AreaOfResidence.unknown
    definition_period = DateUnit.WEEK

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


class accommodation_supplement__cutout(Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.WEEK

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
