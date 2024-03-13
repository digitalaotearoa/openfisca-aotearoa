"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics.housing import AccommodationType


class accommodation_supplement__rate(variables.Variable):
    label = "in relation to a person who is a boarder or lodger in any premises, 62% of the amount paid for board or lodging"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS28903"
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        board_lodger_percent = parameters(period).social_security.accommodation_supplement.board_lodger_percent
        accommodation_type = people("accommodation_type", period)
        not_board = (accommodation_type != AccommodationType.board) * 1
        not_lodge = (accommodation_type != AccommodationType.lodging) * 1
        not_board_lodging = (not_board + not_lodge) - 1
        not_board_lodging = numpy.clip(not_board_lodging + board_lodger_percent, 0, 1)

        return not_board_lodging
