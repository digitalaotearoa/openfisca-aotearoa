"""TODO: Add missing doctring."""

from openfisca_core import periods, variables
from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act
class social_security__child_with_serious_disability(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Child has serious disability"
    reference = """Social Security Act 1964 Part 1D Child disability allowance 39A
        (1)For the purposes of this section and of sections 39B to 39E, child with a serious disability means a dependent child who
        (a) has a physical or mental disability;
        (b) because of that disability needs constant care and attention; and
        (c) is likely to need such care and attention permanently or for a period exceeding 12 months.
        """


# TODO: Review against the new 2018 act
class social_security__disability_self_inflicted(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = """The person's restricted capacity for work, or total blindness, was self-inflicted and brought about by
    the person with a view to qualifying for a benefit"""
    reference = """
        40B (5) A person must not be granted a supported living payment under this section if the chief
        executive is satisfied that the person's restricted capacity for work, or total blindness, was
        self-inflicted and brought about by the person with a view to qualifying for a benefit.
    """
