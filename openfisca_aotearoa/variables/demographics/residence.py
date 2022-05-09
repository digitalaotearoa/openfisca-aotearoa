"""TODO: Add missing doctring."""

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.periods import ETERNITY
from openfisca_core.variables import Variable

# Import the entities specifically defined for this tax and benefit system
from openfisca_aotearoa.entities import Person


class number_of_years_lived_in_nz(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = u"Number of years lived in NZ"


class total_number_of_years_lived_in_nz_since_age_20(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = u"Total number of years lived in NZ since age 20"


class total_number_of_years_lived_in_nz_since_age_50(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = u"Total number of years lived in NZ since age 50"
