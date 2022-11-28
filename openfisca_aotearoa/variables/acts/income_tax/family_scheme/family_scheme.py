"""TODO: Add missing doctring."""

from openfisca_core import holders
from openfisca_core import periods
from openfisca_core.populations import DIVIDE
from openfisca_core import variables

from openfisca_aotearoa import entities


class family_scheme__base_qualifies(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is a person qualified as eligible under the family scheme"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518477.html"

    def formula(persons, period, parameters):
        age_qualifies = persons("family_scheme__caregiver_age_qualifies", period)
        principle_carer = persons("family_scheme__qualifies_as_principal_carer", period)
        residence = persons("income_tax__residence", period)  # this is for caregiver OR child, clarify the test

        return age_qualifies * principle_carer * residence


class family_scheme__caregiver_age_qualifies(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is a person qualified under the family scheme age parameters"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518479.html#DLM1518479"

    def formula(persons, period, parameters):
        return persons("age", period.start) >= parameters(period).entitlements.income_tax.family_scheme.principal_caregiver_age_threshold


class family_scheme__qualifies_as_principal_carer(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is the person the principal caregiver and do they have dependent children"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518480.html"

    def formula(persons, period, parameters):
        return persons("income_tax__principal_caregiver", period) * persons.family("family_scheme__dependent_children", period)


class family_scheme__full_time_earner(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Does the hours per week the person is employed for qualify them as a full time earner"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518419.html"

    def formula(persons, period, parameters):
        has_partner = persons("in_a_relationship", period.first_week) == 1
        hours_per_week_threshold = parameters(period).entitlements.social_security.family_scheme.hours_per_week_threshold
        hours_per_week_threshold_with_partner = parameters(period).entitlements.social_security.family_scheme.hours_per_week_threshold_with_partner

        return ((has_partner == 0) * (persons("hours_per_week_employed", period) >= hours_per_week_threshold)) +\
            ((has_partner > 0) * (persons.family.sum(persons.family.members("hours_per_week_employed", period), role = entities.Family.PARTNER) >= hours_per_week_threshold_with_partner))


class family_scheme__assessable_income(variables.Variable):
    # base_function = missing_value # missing value removed from OpenFisca model_api
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "The annual net income for a person as relates to the family scheme"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518454.html#DLM1518454"
    # Allows user to declare a salary for a year. OpenFisca will spread the yearly amount over the months contained in the year.
    set_input = holders.set_input_divide_by_period

    # TODO there is a myriad of conditions on this variable that represent a large body of work.
    # def formula(person, period, parameters):
    # See legislation reference above however currently "A person’s family scheme income is an amount
    # based on their net income" is possibly the most common use case scenario
    # return person("income_tax__net_income", period)


class family_scheme__assessable_income_for_month(variables.Variable):
    # base_function = missing_value # missing value removed from OpenFisca model_api
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "The monthly net income for a person as relates to the family scheme"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518454.html#DLM1518454"

    def formula(persons, period, parameters):
        return persons("family_scheme__assessable_income", period.this_year, options = [DIVIDE])


class family_scheme__assessable_income_for_week(variables.Variable):
    # base_function = missing_value # missing value removed from OpenFisca model_api
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    label = "The monthly net income for a person as relates to the family scheme"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518454.html#DLM1518454"

    def formula(persons, period, parameters):
        return persons("family_scheme__assessable_income", period.this_year, options = [DIVIDE])


class family_scheme__dependent_children(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.DateUnit.MONTH
    label = "A family has one or more people who qualify as financially dependent children"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518480.html"

    def formula(families, period, parameters):
        return families.max(families.members("income_tax__dependent_child", period.start))
