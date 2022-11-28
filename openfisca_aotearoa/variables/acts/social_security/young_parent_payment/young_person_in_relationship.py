"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act
class young_parent_payment__relationship_requirements(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    label = "Meets Young Parent Payment single person requirements from section 165"
    reference = "https://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM4686082"

    def formula(persons, period, parameters):

        ssa_166_a = numpy.logical_not(persons("in_a_relationship", period.first_week)) * persons("social_security__been_married_or_civil_union_or_de_facto_relationship", period)

        ssa_166_b = persons("in_a_relationship", period.first_week) * numpy.logical_not(persons("social_security__spouse_is_a_specified_beneficiary", period))

        return ssa_166_a + ssa_166_b
