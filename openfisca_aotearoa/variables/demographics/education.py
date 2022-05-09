"""TODO: Add missing doctring."""

from datetime import date

from openfisca_core.periods import ETERNITY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class finish_date_of_full_time_study_training_bridging_18th_birthday(Variable):
    value_type = date
    entity = Person
    definition_period = ETERNITY
    label = "The date a person finished uninterrupted study, as per defintion acc__in_full_time_study"
