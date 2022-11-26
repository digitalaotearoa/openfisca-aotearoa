"""TODO: Add missing doctring."""

import numpy

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import housing


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
        ssa2018_sched_4_part_7_1_to_3 = (
            + numpy.array([cond_1, cond_2, cond_3])
            * rent_board_lodge
            )

        # And conditions 4-6.
        mortgage = accommodation_type == housing.AccommodationType.mortgage
        ssa2018_sched_4_part_7_4_to_6 = (
            + numpy.array([cond_1, cond_2, cond_3])
            * mortgage
            )

        # Finally we create a list of conditions and situations.
        conditions = (
            *ssa2018_sched_4_part_7_1_to_3,
            *ssa2018_sched_4_part_7_4_to_6,
            )
        situations = tuple(AccommodationSupplement__Situation)[1:]
        fallback = AccommodationSupplement__Situation.unknown

        # And we return the situations corresponding to the conditions.
        return numpy.select(conditions, situations, fallback)
