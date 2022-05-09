"""TODO: Add missing doctring."""

from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class hours_per_week_employed(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = u'The hours per week a person is employed for'
