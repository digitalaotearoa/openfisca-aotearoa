"""TODO: Add missing doctring."""

from datetime import date

from openfisca_core import periods, variables

from openfisca_aotearoa.entities import Person


class finish_date_of_full_time_study_training_bridging_18th_birthday(variables.Variable):
    value_type = date
    entity = Person
    definition_period = periods.ETERNITY
    label = "The date a person finished uninterrupted study, as per defintion acc__in_full_time_study"


class early_childcare_hours_participation_per_week(variables.Variable):
    value_type = int
    entity = Person
    definition_period = periods.WEEK
    label = "Number of hours per week person is participating in approved early-childhood education programmes"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282547"


class attending_school(variables.Variable):
    value_type = bool
    entity = Person
    definition_period = periods.WEEK
    label = "Is child attending school"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"


class intends_to_enroll_in_school(variables.Variable):
    value_type = bool
    entity = Person
    definition_period = periods.ETERNITY
    label = "It is intended to enroll the child in a school that has a cohort entry policy in place"
    reference = [
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"  # 2004
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96309"  # 2018
        "https://ref.synco.pt/nz/ssar/168/en/?#P2-S6-s30-p1-b"  # 2018 alternative
        "https://www.workandincome.govt.nz/map/income-support/extra-help/childcare-assistance-programme/qualifications-01.html"  # 2018 Work and Income Guide
        ]
