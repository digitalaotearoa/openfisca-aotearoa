# -*- coding: utf-8 -*-

from openfisca_core.model_api import Variable
from openfisca_core.periods import DAY, MONTH, ETERNITY
from openfisca_aotearoa.entities import Person


class citizenship__citizenship_by_grant_may_be_authorized(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"

    def formula_2005_04_20(persons, period, parameters):
        return persons('age', period) >= parameters(period).citizenship.by_grant.minimum_age_threshold * \
            persons('is_of_full_capacity', period) * \
            persons('citizenship__meets_minimum_presence_requirements', period) * \
            persons('citizenship__is_of_good_character', period) * \
            persons('citizenship__has_sufficient_knowledge_of_the_responsibilities_and_privileges_attaching_to_nz_citizenship') * \
            persons('citizenship__has_sufficient_knowledge_of_the_english_language', period) * \
            (persons('citizenship__intends_to_reside_in_nz', period) + persons('citizenship__intends_to_enter_or_continue_crown_service', period))


class citizenship__meets_minimum_presence_requirements(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = u"Applicant was present in New Zealand for a min of 1,350 days during the 5 years immediately preceding the date of application"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"

    def formula(persons, period, parameters):
        # that the applicant was present in New Zealand—
        # (i) for a minimum of 1350 days during the 5 years immediately preceding the date of the application; and
        # persons('immigration__entitled_to_stay_indefinitely', period) * \
        # (ii) for at least 240 days in each of those 5 years,—
        # being days during which the applicant was entitled in terms of the Immigration Act 2009 to be in New Zealand indefinitely
        # for p in [period.offset(offset) for offset in range(-365, 1)]:

        return persons('days_present_in_new_zealand_in_preceeding_5_years', period) >= parameters(period).citizenship.by_grant.minimum_days_present_in_preceeding_5_years


class days_present_in_new_zealand_in_preceeding_5_years(Variable):
    value_type = int
    entity = Person
    definition_period = DAY

    def formula(persons, period, parameters):

        sum = 0
        for p in [period.offset(offset) for offset in range((days_since_n_years_ago(period, 5) * -1), 1)]:
            sum += (persons('present_in_new_zealand', p) * 1)

        return sum


def days_since_n_years_ago(period, n=1):
    date_n_years_ago = period.date.replace(year=period.date.year - n)
    # The days in that rolling year could  be 365 or 366
    days = (period.date - date_n_years_ago).days - 1 #  subtract one to not include that day
    return days


class days_present_in_new_zealand_in_preceeding_year(Variable):
    value_type = int
    entity = Person
    definition_period = DAY
    label = "was present this many days in the last year"
    reference = "Accumlative from `present_in_new_zealand` variable`"
    default_value = 0

    def formula(persons, period, parameters):

        sum = 0

        # print("{} to {} = {} days".format(one_year_ago, period.date, days_since_n_years_ago))
        for p in [period.offset(offset) for offset in range((days_since_n_years_ago(period) * -1), 1)]:
            sum += (persons('present_in_new_zealand', p) * 1)
        return sum


class present_in_new_zealand(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    default_value = False
    label = "was present in New Zealand on this day"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class immigration__holds_indefinite_stay_visa(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "is entitled in terms of the Immigration Act 2009 to be in New Zealand indefinitely"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__is_of_good_character(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "is of good character"
    reference = ["http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html", "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443872.html"]


class citizenship__has_sufficient_knowledge_of_the_responsibilities_and_privileges_attaching_to_nz_citizenship(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "has sufficient knowledge of the responsibilities and privileges attaching to New Zealand citizenship"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__has_sufficient_knowledge_of_the_english_language(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "has sufficient knowledge of the English language"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__intends_to_reside_in_nz(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "intends to continue to reside in New Zealand"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__intends_to_enter_or_continue_crown_service(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "intends to enter into or continue in Crown service under the New Zealand Government, or service under an international organisation of which the New Zealand Government is a member, or service in the employment of a person, company, society, or other body of persons resident or established in New Zealand"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"
