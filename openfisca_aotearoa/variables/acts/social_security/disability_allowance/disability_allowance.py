"""This module provides eligibility for Disability Allowance."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from operator import truediv
from openfisca_core import periods, variables
from openfisca_core import holders

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities

import numpy

from openfisca_core import holders


# We define the `disability_allowance` variable.
#
# Please note that by itself a `variable` is not a rule but just a
# specification of such a rule.
#
# A `variable` can contain several rules, otherwise called `formulas`, that is,
# several ways it can be calculated, depending on ther date at which we want to
# calculate it. Said otherwise, as a `concept`, any modelled benefit like
# `jobseeker_support` exist since big bang until big crunch, yet the way of
#  calculating it depends on the applicable law at the requested `period`.
#
# For more information on OpenFisca's `variables`:
# https://openfisca.org/doc/key-concepts/variables.html
class disability_allowance__entitled(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Disability Allowance eligibility"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783266"

    def formula_2018_11_26(persons, period, parameters):

        ssa2018_85_2_a_i = persons("disability_allowance__needs_ongoing_support", period)
        ssa2018_85_2_a_ii = persons("disability_allowance__needs_ongoing_treatment", period)
        ssa2018_85_2_b = persons("disability_allowance__continuing_disability", period)
        ssa2018_85_2_c_i = persons("social_security__granted_main_benefit", period)
        ssa2018_85_2_c_ii = persons("disability_allowance__below_income_threshold", period)
        ssa2018_85_2_d = persons("disability_allowance__ongoing_additional_expenses", period)
        
        return (ssa2018_85_2_a_i + ssa2018_85_2_a_ii) * ssa2018_85_2_b * ((ssa2018_85_2_c_i) + (ssa2018_85_2_c_ii)) * ssa2018_85_2_d


class disability_allowance__needs_ongoing_support(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person need ongoing support to undertake the everyday functions of life?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__needs_ongoing_treatment(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person need ongoing supervision or treatment by a health practitioner?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__continuing_disability(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the disability likely to continue for at least 6 months?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__below_income_threshold(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Person's income meets the thresholds as specified in Part 3 (Disability Allowance Income Limits) of the SS Act 2018"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280" 

    def formula_2018_11_26(persons, period, parameters):
        meets_clause_10_conditions = persons("disability_allowance__income_limit_clause_10", period) #single person (16/17) w/out dep children
        meets_clause_11_conditions = persons("disability_allowance__income_limit_clause_11", period) #single person w/out dep children
        meets_clause_12_conditions = persons("disability_allowance__income_limit_clause_12", period) #in relationship
        meets_clause_13_conditions = persons("disability_allowance__income_limit_clause_13", period) #single person with 1 child
        meets_clause_14_conditions = persons("disability_allowance__income_limit_clause_14", period) #single person with > 1 child

        return meets_clause_10_conditions + meets_clause_11_conditions + meets_clause_12_conditions 
        + meets_clause_13_conditions + meets_clause_14_conditions


class disability_allowance__ongoing_additional_expenses(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person have additional expenses of an ongoing kind arising from the person’s disability?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"



class disability_allowance__person_entitled_to_reciprocal_benefits(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Reciprocal benefits for person entitled to reciprocal benefits"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


# class disability_allowance__receiving_any_other_disability_allowance(variables.Variable):
#     value_type = bool
#     default_value = False
#     entity = entities.Person
#     definition_period = periods.WEEK
#     label = "Reciprocal benefits for person entitled to reciprocal benefits"
#     reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


# class disability_allowance__receiving_accident_compensation_entitlement(variables.Variable):
#     value_type = bool
#     default_value = False
#     entity = entities.Person
#     definition_period = periods.WEEK
#     label = "Is the person receiving accident compensation entitlement?"
#     reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


# class disability_allowance__receiving_disablement_pension(variables.Variable):
#     value_type = bool
#     default_value = False
#     entity = entities.Person
#     definition_period = periods.WEEK
#     label = "Is the person receiving a disablement pension under Part 3?"
#     reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


# class disability_allowance__receiving_veterans_support_entitlement(variables.Variable):
#     value_type = bool
#     default_value = False
#     entity = entities.Person
#     definition_period = periods.WEEK
#     label = "Is the person receiving an entitlement under Part 4 of the Veterans’ Support Act 2014?"
#     reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__income_limit_clause_10(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per clause 10?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"

    def formula_2018_11_26(persons, period, parameters):
        person_aged_16_or_17 = (persons("age", period.start) >= 16) * (persons("age", period.start) <= 17) 
        no_partners = numpy.logical_not(persons("social_security__in_a_relationship", period))
        income_within_limit = persons("social_security__income", period) <= parameters(period).disability_allowance.income_limits.clauses["clause_10"]
        without_dependant_child = persons("social_security__dependent_children", period) == 0
        return person_aged_16_or_17 * no_partners * income_within_limit * without_dependant_child 

class disability_allowance__income_limit_clause_11(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per clause 11?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"

    def formula_2018_11_26(persons, period, parameters):
        person_not_aged_16_or_17 = (persons("age", period.start) < 16) + (persons("age", period.start) > 17)
        no_partners = numpy.logical_not(persons("social_security__in_a_relationship", period))
        without_dependant_child = persons("social_security__dependent_children", period) == 0
        not_a_child = numpy.logical_not(persons.has_role(entities.Family.CHILD))  #review this
        income_within_limit = persons("social_security__income", period) <= parameters(period).disability_allowance.income_limits.clauses["clause_11"]
        return person_not_aged_16_or_17 * no_partners * without_dependant_child * income_within_limit * not_a_child


class disability_allowance__income_limit_clause_12(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per clause 12?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"

    def formula_2018_11_26(persons, period, parameters):
        in_relationship = persons("social_security__in_a_relationship", period)
        income_within_limit = persons("disability_allowance__family_income", period) <= parameters(period).disability_allowance.income_limits.clauses["clause_12"]
        return in_relationship * income_within_limit


class disability_allowance__income_limit_clause_13(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per clause 13?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"

    def formula_2018_11_26(persons, period, parameters):
        sole_parent = persons("is_sole_parent", period) * \
        persons("disability_allowance__sole_parent_meets_relationship_qualification", period)
        only_one_child = (persons("social_security__dependent_children", period) == 1)
        income_within_limit = persons("social_security__income", period) <= parameters(period).disability_allowance.income_limits.clauses["clause_13"]
        return income_within_limit * only_one_child * sole_parent


class disability_allowance__income_limit_clause_14(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per clause 14?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"

    def formula_2018_11_26(persons, period, parameters):
        sole_parent = persons("is_sole_parent", period) * \
        persons("disability_allowance__sole_parent_meets_relationship_qualification", period)
        more_than_one_child = (persons("social_security__dependent_children", period) > 1)
        income_within_limit = persons("social_security__income", period) <= parameters(period).disability_allowance.income_limits.clauses["clause_14"]
        return more_than_one_child * sole_parent * income_within_limit


class disability_allowance__is_adequately_supported_by_partner(variables.Variable):
    value_type = bool
    entity = entities.Person
    default_value: False
    label = """Is adequately supported by their partner? (false if lost the regular support of
    their partner as their partner has been imprisoned or is subject to release or detention conditions that prevent employment)
    """
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784375.html"


class disability_allowance__sole_parent_meets_relationship_qualification(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Meets the sole parent support test for not being in a relationship"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784375.html"

    def formula(persons, period, parameters):
        # Do they have a partner
        no_partners = (persons("social_security__in_a_relationship", period) == 0)
        not_supported = (persons("disability_allowance__is_adequately_supported_by_partner", period) == 0)
        # no partner, OR not supported by partner
        return no_partners + not_supported


class disability_allowance__family_income(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "How much does the family earn per week?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"   

    def formula(people, period, parameters):
        family_income = people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PARTNER) + \
        people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PRINCIPAL) 
        return family_income


class disability_allowance__benefit(variables.Variable):
    value_type = float
    default_value = -9999
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Maximum disability allowance that a person is eligible for."
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"

    def formula_2018_11_26(persons, period, parameters):

        return persons("disability_allowance__entitled", period) * parameters(period).disability_allowance.max_weekly_benefit


class is_sole_parent(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the person a sole parent?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784375.html"