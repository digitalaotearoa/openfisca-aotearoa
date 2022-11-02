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
class disability_allowance_entitled(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Disability Allowance eligibility"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783145", "https://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363196.html#DLM363196"

    # Disability has the same meaning as in section 21(1)(h) of the Human Rights Act 1993: https://www.legislation.govt.nz/act/public/1993/0082/latest/DLM304475.html#DLM304475
    def formula_2018_11_26(persons, period, parameters):

        ssa2018_85_2_a_i = persons('disability_allowance__needs_ongoing_support', period)
        ssa2018_85_2_a_ii = persons('disability_allowance__needs_ongoing_treatment', period)
        ssa2018_85_2_b = persons('disability_allowance__continuing_disability', period)
        ssa2018_85_2_c_i = persons('disability_allowance__receives_main_benefit', period)
        ssa2018_85_2_c_ii = persons('disability_allowance__below_income_threshold', period)
        ssa2018_85_2_d = persons('disability_allowance__ongoing_additional_expenses', period)
        ssa2018_87_a = numpy.logical_not(persons('disability_allowance__receiving_disablement_pension' , period))
        ssa2018_87_b = numpy.logical_not(persons('disability_allowance__receiving_accident_compensation_entitlement', period))
        ssa2018_87_c_i_to_iii = numpy.logical_not(persons('disability_allowance__receiving_any_other_disability_allowance', period))

        return (ssa2018_85_2_a_i + ssa2018_85_2_a_ii) * ssa2018_85_2_b * ((ssa2018_85_2_c_i) + (ssa2018_85_2_c_ii)) * ssa2018_85_2_d \
        * ssa2018_87_a * ssa2018_87_b * ssa2018_87_c_i_to_iii

class disability_allowance__needs_ongoing_support(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person need ongoing support to undertake the everyday functions of life?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__receives_main_benefit(variables.Variable): # need to re-factor
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__needs_ongoing_treatment(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person need ongoing supervision or treatment by a health practitioner?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__ongoing_additional_expenses(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person have additional expenses of an ongoing kind arising from the person’s disability?"
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
    label = "Is the person's income below income threshold specified from ?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280" 


class disability_allowance__income_limit_clause_10(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per subpart 10?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        
        person_aged_16_or_17 = (persons("age", period.start) >= 16) * (persons("age", period.start) <= 17) 
        no_partners = (persons("disability_allowance__person_has_partner", period) == 0) #review this
        income_within_limit = persons("disability_allowance__current_income", period) <= parameters(period).disability_allowance.income_limits.single_person.no_children.within_age_limit
        # without_dependant_child = persons.families.nb_persons(role=Family.CHILD) == 0
        return person_aged_16_or_17 * no_partners * income_within_limit # * without_dependant_child 

class disability_allowance__income_limit_clause_11(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per subpart 11?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        
        no_partners = numpy.logical_not(persons("disability_allowance__person_has_partner", period) == 0) #review this
       # without_dependent_child = numpy.logical_not(persons("disability_allowance__person_has_dependant_child", period)) # review
        without_dependant_child = (persons.has_role(entities.Family.CHILD) == 0)
        income_within_limit = persons("disability_allowance__current_income", period) <= parameters(period).disability_allowance.income_limits.single_person.no_children.outside_age_limit
        return no_partners * without_dependant_child * income_within_limit


class disability_allowance__income_limit_clause_12(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per subpart 12?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        
        in_relationship = persons("disability_allowance__person_has_partner", period) #review this
        income_within_limit = persons("disability_allowance__current_income", period) <= parameters(period).disability_allowance.income_limits.in_a_relationship
        return in_relationship * income_within_limit


class disability_allowance__person_has_dependant_child(variables.Variable): #refactor to make re-usable
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
    label = "Does the person have a dependant child?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"


class disability_allowance__income_limit_clause_13(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per subpart 13?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        
        income_within_limit = persons("disability_allowance__current_income", period) <= parameters(period).disability_allowance.income_limits.single_person.sole_parent_with_one_dep_child
        return income_within_limit * (persons.has_role(entities.Family.CHILD) >= 1)


class disability_allowance__income_limit_clause_14(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person earn below the Disability Allowance Income Limit as per subpart 14?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        
        in_relationship = persons("disability_allowance__person_has_partner", period) #review this
        income_within_limit = persons("disability_allowance__current_income", period) <= parameters(period).disability_allowance.income_limits.single_person.sole_parent_with_one_dep_child
        return in_relationship * income_within_limit * (persons.has_role(entities.Family.CHILD) >= 1)


class disability_allowance__person_has_children(variables.Variable): #stopgap duplicate variable until weeks/months issue is resolved.
    value_type = int # look into how social_security__person_has_dependant_child is structured by removing set input dispatch by period
    entity = entities.Person
    label = "Does this person have more than one child?"
    definition_period = periods.WEEK
    reference = "TODO"

    def formula(persons, period, parameters):
        return number_of_children == (persons.has_role(entities.Family.CHILD) >= 1)


class disability_allowance__current_income(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.WEEK
    label = "How much does the person earn per week?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"   


class disability_allowance__family_income(variables.Variable): # Copied from social security job_seeker formulas
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "How much does the family earn per week?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784890.html"   

    def formula(people, period, parameters):
        family_income = people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PARTNER) + \
        people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PRINCIPAL) 
        return family_income


class disability_allowance__benefit_amount(variables.Variable):
    value_type = int
    default_value = -9999
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Amount that a person is eliglble for"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"

    def formula_2018_11_26(persons, period, parameters):

        return numpy.select([persons("disability_allowance__age_meets_criteria", period)], [588])


class disability_allowance__person_entitled_to_reciprocal_benefits(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Reciprocal benefits for person entitled to reciprocal benefits"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"

class disability_allowance__receiving_any_other_disability_allowance(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Reciprocal benefits for person entitled to reciprocal benefits"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__receiving_accident_compensation_entitlement(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the person receiving accident compensation entitlement?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"

class disability_allowance__receiving_disablement_pension(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the person receiving disablement pension?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__person_has_partner(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person have a partner?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


class disability_allowance__person_has_children(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Does the person have children?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"


# class test_b(variables.Variable):
#     value_type = bool
#     default_value = False
#     entity = entities.Person
#     definition_period = periods.MONTH
#     label = "Does the person need ongoing support to undertake the everyday functions of life"
#     reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783280"

#     def formula(persons, period, parameters):
#         return persons('person_has_partner' , period)

# 	For a single person aged 16 or 17 years without dependent children		$588.98
# 11	For any other single person without dependent children		$733.72
# 12	For a person who is in a relationship with or without dependent children		$1,092.55
# 13	For a sole parent with 1 dependent child		$821.43
# 14	For any other sole parent		$865.46