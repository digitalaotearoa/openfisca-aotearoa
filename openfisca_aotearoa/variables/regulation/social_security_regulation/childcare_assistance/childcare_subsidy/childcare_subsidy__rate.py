"""Formula for establishing the rate of childcare subsidy."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class childcare_subsidy__maximum(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Maximum childcare subsidy available calculated from possible payable hours"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96315"  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s36"  # 2018 alt
        "https://ref.synco.pt/nz/ssar/171/en/#sd2"  # 2018 alt
        "https://www.workandincome.govt.nz/map/deskfile/extra-help-information/childcare-assistance-tables/childcare-subsidy-current.html"  # MSD Interpretation
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282551.html",  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        number_of_children_who_meet_criteria = persons.family.sum(persons.family.members("childcare_subsidy__child_meets_criteria", period))
        return persons("childcare_subsidy__hours_payable", period) * persons("childcare_subsidy__rate", period) * number_of_children_who_meet_criteria


class childcare_subsidy__rate(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Maximum hourly rate of childcare subsidy for payable hours, note this can be no more than the actual hourly fee payable"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96315"  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s36"  # 2018 alt
        "https://ref.synco.pt/nz/ssar/171/en/#sd2"  # 2018 alt
        "https://www.workandincome.govt.nz/map/deskfile/extra-help-information/childcare-assistance-tables/childcare-subsidy-current.html"  # MSD Interpretation
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282551.html",  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        dependant_children = persons("social_security__dependent_children", period)
        household_income = persons.family("social_security_regulation__household_income", period)
        scale_1child = parameters(period).social_security.childcare_assistance.rates_onechild
        scale_2child = parameters(period).social_security.childcare_assistance.rates_twochildren
        scale_3child = parameters(period).social_security.childcare_assistance.rates_threepluschildren

        onechild = dependant_children == 1
        twochildren = dependant_children == 2
        threepluschildren = dependant_children >= 3

        return (scale_1child.calc(household_income) * onechild) + (scale_2child.calc(household_income) * twochildren) + (scale_3child.calc(household_income) * threepluschildren)
