"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class family_scheme__qualifies_for_child_tax_credit(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is a person qualified as eligible for the child tax credit"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518622.html#DLM1518622"

    def formula(persons, period, parameters):
        # TODO there are additional conditions as outlined in the reference
        return persons("family_scheme__base_qualifies", period)


class family_scheme__child_tax_credit_entitlement(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "The child tax credit entitlement a person has under the family scheme"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518624.html#DLM1518624"

    def formula(persons, period, parameters):
        # TODO
        return persons
