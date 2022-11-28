"""TODO: Add missing doctring."""

import datetime

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class finish_date_of_full_time_study_training_bridging_18th_birthday(variables.Variable):
    value_type = datetime.date
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "The date a person finished uninterrupted study, as per defintion acc__in_full_time_study"


class early_childcare_hours_participation_per_week(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Number of hours per week person is participating in approved early-childhood education programmes"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282547"


class attending_school(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is child attending school"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"


class will_be_enrolled_in_school(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Child will be enrolled in a school that has a cohort entry policy in place"
    # (ba) who is 5, whose parent, principal caregiver, or guardian intends to enrol
    # the child in a school that has a cohort entry policy in place, and who
    # (under section 5B(2) of the Education Act 1989) may not be enrolled in that
    # school until the term start date of the next term;"""
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"
