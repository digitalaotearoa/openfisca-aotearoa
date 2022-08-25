"""TODO: Add missing doctring."""

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the entities specifically defined for this tax and benefit system
from openfisca_aotearoa.entities import Family, Person


# Re-usable variable for having a partner
class person_has_partner(Variable):
    value_type = bool
    entity = Person
    label = "Is this person in a relationship?"
    definition_period = MONTH  # This variable changes over time.
    reference = "TODO"

    def formula(persons, period, parameters):
        # has 1 or more partners
        number_of_partners = persons.family.nb_persons(role=Family.PARTNER)
        return number_of_partners >= 1


class is_adequately_supported_by_partner(Variable):
    value_type = bool
    entity = Person
    label = """Is adequately supported by their partner? (false if lost the regular support of
    their partner as their partner has been imprisoned or is subject to release or detention conditions that prevent employment)
    """
    definition_period = MONTH
    reference = "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/qualifications.html"
    default_value = True


class person_is_parent(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is a parent?"


class is_a_step_parent(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is a step-parent?"


class married(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is married?"

    def formula(persons, period, parameters):
        return persons("marriage__married", period)


class civil_union(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is in a civil union?"

    def formula(persons, period, parameters):
        return persons("civil_union__civil_union", period)


class de_facto_relationship(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is in a de facto relationship?"

    def formula(persons, period, parameters):
        return persons("property_relationships__de_facto_relationship", period)


class has_been_married_or_in_a_civil_union_or_de_facto_relationship(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "He or she is not married but has been married or in a civil union or de facto relationship"


class married_or_civil_union_or_de_facto_relationship(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "He or she is married, or in a civil union or de facto relationship"

    def formula(persons, period, parameters):
        return persons("married", period) + persons("civil_union", period) + persons("de_facto_relationship", period)
