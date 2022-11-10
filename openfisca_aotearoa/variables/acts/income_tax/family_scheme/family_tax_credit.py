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

    def formula_2007_11_01(people, period, parameters):
        return (
            + people("family_tax_credit__eligible", period)
            * people("family_tax_credit__base", period)
            )


class family_tax_credit__eligible(Variable):
    label = "Is person eligible for family tax credit? (y/n)"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = "https://www.wikidata.org/wiki/Q115148845"
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.YEAR


class family_tax_credit__base(Variable):
    label = "Amount of family tax credit, not considering eligibility, abatement, or reductions"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = "https://www.wikidata.org/wiki/Q115148931"
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.YEAR

    def formula_2007_11_01(people, period, parameters):
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
    definition_period = DateUnit.DAY

    def formula_2007_11_01(people, period, params):
        age = people("age", period)
        under_16y = age < 16
        principal = people.has_role(Family.PRINCIPAL)
        caregived = people("family_tax_credit__dependent_child", period.this_year)
        dependent = caregived >= 100 / 3 - .5  # last value is the error margin
        eldest_child = sum(under_16y * dependent) - 1 >= 0
        
        prescribed_amount = (
            params(period)
            .acts
            .income_tax
            .family_tax_credit
            .prescribed_amount
            .eldest
            )
        
        return (
            + principal
            * eldest_child
            * prescribed_amount
            / period.this_year.days
            )


class family_tax_credit__not_eldest(Variable):
    label = "Amount of family tax credit for not eldest child, not considering eligibility, abatement, or reductions"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518515.html#DLM1518515"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.DAY

    def formula_2007_11_01(people, period, parameters):
        age = people("age", period)
        under_16y = age < 16
        principal = people.has_role(Family.PRINCIPAL)
        caregived = people("family_tax_credit__dependent_child", period.this_year)
        dependent = caregived >= 100 / 3 - .5  # last value is the error margin
        other_than_the_eldest_child = max([0, sum(under_16y * dependent) - 1])

        prescribed_amount = (
            params(period)
            .acts
            .income_tax
            .family_tax_credit
            .prescribed_amount
            .not_eldest
            )

        return (
            + principal
            * other_than_the_eldest_child
            * prescribed_amount
            / period.this_year.days
            )


class family_tax_credit__dependent_child(Variable):
    label = "Percentage over the rolling year that this child is under principal caregiving by P"
    reference = "https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518492.html"
    documentation = """TODO"""
    entity = Person
    value_type = int
    default_value = 0
    definition_period = DateUnit.YEAR

    ###########################################################################
    #                                                                         #
    # Please note this refers to the following text:                          #
    #                                                                         #
    # For the purposes of sections MD 3, MG 1, and MZ 1 (which relate to      #
    # certain tax credits for families), a person is a principal caregiver of #
    # a dependent child if the person— [...]                                  #
    #                                                                         #
    # (b)   has the dependent child in their exclusive care for periods       #
    #       totalling at least one-third of— [...]                            #
    #                                                                         #
    #       (ii)    the tax year:                                             #
    #                                                                         #
    ###########################################################################


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
