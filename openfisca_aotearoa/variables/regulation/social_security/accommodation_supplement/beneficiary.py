"""Beneficiaries and non-beneficiaries."""
import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__beneficiary(variables.Variable):
    label = "Social Security Regulations 2018 §17.1 Beneficiary"
    reference = "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96264.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        receiving_main_benefit = people("social_security__receiving_main_benefit", period)
        receiving_superannuation = people("super__receiving", period)
        receiving_veterans_pension = people("veterans_pension__receiving", period)

        ssr2018_17_1_a = receiving_main_benefit
        ssr2018_17_1_b = receiving_superannuation + receiving_veterans_pension

        return ssr2018_17_1_a + ssr2018_17_1_b


class accommodation_supplement__non_beneficiary(variables.Variable):
    label = "Social Security Regulations 2018 §17.1 Non-beneficiary"
    reference = "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96264.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        beneficiaries = people("accommodation_supplement__beneficiary", period)

        return numpy.logical_not(beneficiaries)
