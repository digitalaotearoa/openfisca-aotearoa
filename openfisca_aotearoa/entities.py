"""TODO: Add missing doctring."""

# This file defines the entities needed by our legislation.
from openfisca_core.entities import build_entity

# General note about how to consider roles as they are utilised in OpenFisca Aotearoa
#
# Best practice would be to not utilise roles as legal definitions, instead as a framework for structuring scenarios.
#
# For instance, a person in the role of child (family entity) should not be assumed to be a social_security__dependent_child
# or even a social_security__child. Those legal concepts should be required of the persons put in the child role.
#
# In some more generic situations the role can be used to imply a more general concept. For an example of this see: in_a_relationship which will return true if the person occupys the role of partner in a scenario.
# The decision to lean on this variable should be carefully considered in light of the definitions within the instrument of law being interpreted.
# If the instrument has it's own definition for partner - it's probably better to fashion a variable that includes the appropriate tests to that use case.


Person = build_entity(
    key = "person",
    plural = "persons",
    label = "Person",
    doc = """
    A Person represents an individual, the minimal legal entity on which a legislation might be applied.

    Example:
    The "salary" and "income_tax" variables are usually defined for the entity "Person".

    Usage:
    Calculate a variable applied to a "Person" (e.g. access the "salary" of a specific month with person("salary", "2017-05")).
    Check the role of a "Person" in a group entity (e.g. check if a the "Person" is a "owner" in a "Titled_Property" entity with person.has_role(Titled_Property.owner)).

    For more information on entities, see: http://openfisca.org/doc/coding-the-legislation/50_entities.html
    """,
    is_person = True,
    )

Family = build_entity(
    key = "family",
    plural = "families",
    label = "Family",
    doc = """
    A Family represents a collection of related persons.

    Family entities are a way of making calculations across a number of entitlements including for example "Working for families" and "Paid Parental Leave"

    A family can contain a number of roles, such as "principal", "partner" & "child".

    For more information on entities, see: http://openfisca.org/doc/coding-the-legislation/50_entities.html

    Families can be used to make calculations for the principal; as each entitlement is calculated in relation to the Principal it is recommended for modelling to create multiple family sets for each principal if needing to describe scenarios for different family members

    """,
    roles = [
        {
            "key": "principal",
            "label": "Principal",
            "doc": "The one person who is the focus of a calculation in a family context. This is not to be confused with 'principal caregiver' and other such legal terms",
            "max": 1,
            },
        {
            "key": "partner",
            "plural": "partners",
            "label": "Partners",
            "doc": """
            The one or more persons who are partners of the principal.
            Utilise variables to further define if a person fits the legal definition of a partner as it differs between legal instruments.
            In the case of the Social Security Act this can be considered an alternative to "in_a_relationship"
            """,
            },
        {
            "key": "parent",
            "plural": "parents",
            "label": "Parents",
            "doc": """
            The one or more persons who are also parents of children of the principal.
            Utilise variables to further define if a person fits the legal definition of a partner as it differs between legal instruments.
            In the case of the Social Security Act the application of "sole_parent_support__receiving" can be used for either parent to describe their scenario
            """
            },
        {
            "key": "child",
            "plural": "children",
            "label": "Children",
            "doc": """
            The children of a family, in relation to the principal. This is a not a legally defined role but is instead representative of the relationship.
            Utilise variables to further define if a person fits the legal definition of a child as it differs between legal instruments.
              """,
            },
        {
            "key": "other",
            "plural": "others",
            "label": "Other",
            "doc": "All other members of a family/whānau.",
            },
        ],
    )

Tenancy = build_entity(
    key = "tenancy",
    plural = "tenancies",
    label = "Tenancy",
    doc = """TODO""",
    roles = [
        {
            "key": "principal",
            "label": "Principal",
            "doc": "The one person who is the focus of the calculation",
            "max": 1,
            },
        {
            "key": "tenant",
            "plural": "tenants",
            "label": "Tenants",
            "doc": """#TODO""",
            },
        {
            "key": "other",
            "plural": "others",
            "label": "Other",
            "doc": "All other members of a tenancy",
            },
        ],
    )

Ownership = build_entity(
    key = "ownership",
    plural = "ownerships",
    label = "Ownership",
    doc = """TODO""",
    roles = [
        {
            "key": "principal",
            "label": "Principal",
            "doc": "The one person who is the focus of the calculation",
            "max": 1,
            },
        {
            "key": "owner",
            "plural": "owners",
            "label": "Owners",
            "doc": """#TODO""",
            },
        {
            "key": "other",
            "plural": "others",
            "label": "Other",
            "doc": "All other members of an ownership",
            },
        ],
    )

Titled_Property = build_entity(
    key="titled_property",
    plural="titled_properties",
    label="Titled Property",
    doc="""
    A Titled property represents a property that is owned by a Person or group of Persons.

    Example usage:
    Check the number of individuals of a specific role: check how many persons co-own the property: `titled_properties.nb_persons(Titled_Property.OWNER)`.
    Calculate a variable applied to each tenant of the group entity: calculate the income of each member of the Property: `tenants_incomes = titled_properties.members("income", period = MONTH); tenants_total_income = titled_properties.sum(tenants_incomes)`.

    For more information on group entities, see: http://openfisca.org/doc/coding-the-legislation/50_entities.html
    """,
    roles=[
        {
            "key": "owner",
            "plural": "owners",
            "label": "Owners",
            "doc": "The one or more persons who hold title for the property.",
            },
        {
            "key": "other",
            "plural": "others",
            "label": "Others",
            "doc": "People who are not in any other role",
            },
        ],
    )


entities = [Titled_Property, Ownership, Tenancy, Person, Family]
