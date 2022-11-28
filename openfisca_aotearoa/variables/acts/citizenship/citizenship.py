"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import residence

class citizenship__citizen(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = """New Zealand citizen means a person who has New Zealand citizenship as provided in the Citizenship Act 1977 or the Citizenship (Western Samoa) Act 1982"""
    reference = "https://legislation.govt.nz/act/public/1977/0061/latest/whole.html", "https://legislation.govt.nz/act/public/1982/0011/latest/whole.html"


class citizenship__citizenship_by_grant_may_be_authorized(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"
    label = "statisfies criteria such that the Minister may authorise the grant of New Zealand citizenship to this person"

    def formula_2005_04_20(persons, period, parameters):

        return (persons("age", period) >= parameters(period).citizenship.by_grant.minimum_age_threshold) * \
            persons("full_capacity", periods.DateUnit.ETERNITY) * \
            persons("citizenship__minimum_presence_requirements", period) * \
            persons("citizenship__of_good_character", periods.DateUnit.ETERNITY) * \
            persons("citizenship__sufficient_knowledge_responsibilities_and_privileges", periods.DateUnit.ETERNITY) * \
            persons("citizenship__sufficient_knowledge_english_language", periods.DateUnit.ETERNITY) * \
            (persons("citizenship__intends_to_reside_in_nz", periods.DateUnit.ETERNITY) + persons("citizenship__intends_crown_service", periods.DateUnit.ETERNITY)
                + persons("citizenship__intends_international_service", periods.DateUnit.ETERNITY) + persons("citizenship__intends_nz_employment", periods.DateUnit.ETERNITY))


class citizenship__minimum_presence_requirements(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "meets the two presence in NZ requirements within the Citizenship Act"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"

    def formula(persons, period, parameters):
        # persons("immigration__entitled_to_stay_indefinitely", period) * \
        # (ii) for at least 240 days in each of those 5 years,—
        # being days during which the applicant was entitled in terms of the Immigration Act 2009 to be in New Zealand indefinitely
        # for p in [period.offset(offset) for offset in range(-365, 1)]:
        return persons("citizenship__5_year_presence_requirement", period) * \
            persons("citizenship__each_year_minimum_presence_requirements", period)


class citizenship__each_year_minimum_presence_requirements(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "was present in New Zealand for at least 240 days in each the 5 years immediately preceding the date of application "
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"

    def formula(persons, period, parameters):
        required_days = parameters(period).citizenship.by_grant.minimum_days_present_for_each_of_preceeding_5_years

        meets_presence = True

        for n in range(0, 5):
            # print("Checking year", n, "ending on", period.date)

            number_of_days_ago = residence.days_since_n_years_ago(period.date, n)
            # print("the day to end our rolling year on is (the day before)", number_of_days_ago, "days before", period.date)

            # Go back in time by n years
            day_n_years_ago = period.offset(number_of_days_ago * -1)
            # print("day_n_years_ago", day_n_years_ago)

            days_present = persons("days_present_in_new_zealand_in_preceeding_year", day_n_years_ago)
            # print("days present on rolling year ending at", day_n_years_ago, "is", days_present)

            meets_presence_n_years_ago = (days_present >= required_days)
            # print("Meets requirement??", meets_presence_n_years_ago)

            # Accumulate the each year
            meets_presence = meets_presence_n_years_ago * meets_presence

            # print("======================")

        return meets_presence


class citizenship__preceeding_single_year_minimum_presence_requirement(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "was present in New Zealand for at least 240 days in one rolling year immediately preceding the date of application "
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"

    def formula(persons, period, parameters):
        required_days = parameters(period).citizenship.by_grant.minimum_days_present_for_each_of_preceeding_5_years
        return persons("days_present_in_new_zealand_in_preceeding_year", period) >= required_days


class citizenship__5_year_presence_requirement(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY

    label = "was present in New Zealand for a minimum of 1,350 days during the 5 years immediately preceding the date of the application"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"

    def formula(persons, period, parameters):
        # that the applicant was present in New Zealand—
        # (i)  and
        required_days = parameters(period).citizenship.by_grant.minimum_days_present_in_preceeding_5_years
        days_present = persons("days_present_in_new_zealand_in_preceeding_5_years", period)

        return days_present >= required_days


class citizenship__of_good_character(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "is of good character"
    reference = ["http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html", "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443872.html"]


class citizenship__sufficient_knowledge_responsibilities_and_privileges(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "has sufficient knowledge of the responsibilities and privileges attaching to New Zealand citizenship"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__sufficient_knowledge_english_language(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "has sufficient knowledge of the English language"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__intends_to_reside_in_nz(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "intends to continue to reside in New Zealand"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__intends_crown_service(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "intends to enter into or continue in Crown service under the New Zealand Government"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__intends_international_service(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "intends to enter into or continue service under an international organisation of which the New Zealand Government is a member"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"


class citizenship__intends_nz_employment(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "intends to enter into or continue service in the employment of a person, company, society, or other body of persons resident or established in New Zealand"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"
