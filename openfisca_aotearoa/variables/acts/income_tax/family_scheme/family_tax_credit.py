"""TODO: Add missing doctring."""

from openfisca_core import holders
from openfisca_core.periods import DateUnit
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person, Family


class family_tax_credit(Variable):
    label = "Amount of family tax credit, considering eligibility, abatement, and reductions"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518514.html"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.YEAR

    def formula(people, period, parameters):
        return (
            + people("family_tax_credit__eligible", period)
            * people("family_tax_credit__base", period)
            )


class family_tax_credit__eligible(Variable):
    label = "Is person eligible for family tax credit? (y/n)"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = """TODO"""
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.YEAR


class family_tax_credit__base(Variable):
    label = "Amount of family tax credit, not considering eligibility, abatement, or reductions"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.YEAR

    def formula(people, period, parameters):
        return (
            + people("family_tax_credit__eldest", period, "add")
            + people("family_tax_credit__not_eldest", period, "add")
            )


class family_tax_credit__eldest(Variable):
    label = "Amount of family tax credit for eldest child, not considering eligibility, abatement, or reductions"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.WEEKDAY

    def formula(people, period, parameters):
        age = people("age", period.first_day)
        under_16y = age < 16
        dependent = people("social_security__dependent_child", period.first_week)

        return (
            + people.has_role(Family.PRINCIPAL)
            * (sum(under_16y * dependent) - 1 >= 0)
            * 6642
            / 365
            )


class family_tax_credit__not_eldest(Variable):
    label = "Amount of family tax credit for not eldest child, not considering eligibility, abatement, or reductions"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.WEEKDAY

    def formula(people, period, parameters):
        age = people("age", period.first_day)
        under_16y = age < 16
        dependent = people("social_security__dependent_child", period.first_week)

        return (
            + people.has_role(Family.PRINCIPAL)
            * max([0, sum(under_16y * dependent) - 1])
            * 5412
            / 365
            )


class family_scheme__qualifies_for_family_tax_credit(Variable):
    value_type = bool
    entity = Person
    definition_period = DateUnit.MONTH
    label = "Is a person qualified as eligible for the family tax credit"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"

    def formula(persons, period, parameters):
        return persons("family_scheme__base_qualifies", period) *\
            persons("family_scheme__family_tax_credit_income_under_threshold", period)


class family_scheme__family_tax_credit_income_under_threshold(Variable):  # this variable is a proxy for the calculation "family_scheme__family_tax_credit_entitlement" which needs to be coded
    value_type = bool
    entity = Person
    definition_period = DateUnit.MONTH
    label = "Is the person income under the threshold for the family tax credit"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518484.html"


class family_scheme__family_tax_credit_entitlement(Variable):
    value_type = float
    entity = Person
    definition_period = DateUnit.MONTH
    label = "The family tax credit person is entitlement to under the family scheme"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518514.html"

    def formula(persons, period, parameters):
        # eldest_child_credit = parameters(period).entitlements.income_tax.family_scheme.family_tax_credit.eldest_child
        # subsequent_child_credit = parameters(period).entitlements.income_tax.family_scheme.family_tax_credit.subsequent_child
        # threshold = parameters(period).entitlements.income_tax.family_scheme.family_tax_credit.full_year_abatement_threshold
        # rate = parameters(period).entitlements.income_tax.family_scheme.family_tax_credit.full_year_abatement_rate

        # sum up families income
        # http://legislation.govt.nz/act/public/2007/0097/latest/DLM1518488.html#DLM1518488
        # family_income = persons.family.sum(persons.family.members("family_scheme__assessable_income", period.this_year))

        # calculate income over the threshold
        # income_over_threshold = where((family_income - threshold) < 0, 0, family_income - threshold)

        # calculate the number of children
        number_of_children = persons.family.sum(
            persons("income_tax__dependent_child", period))

        # TODO this variable is incomplete and requires the formula to be finished
        return number_of_children
