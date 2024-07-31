"""
This file defines our country's tax and benefit system.

A tax and benefit system is the higher-level instance in OpenFisca.
Its goal is to model the legislation of Aotearoa.
Basically a tax and benefit system contains simulation variables (source code) and legislation parameters (data).

See https://openfisca.org/doc/key-concepts/tax_and_benefit_system.html
"""

import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_aotearoa.conf.cache_blacklist import \
    cache_blacklist as conf_cache_blacklist
from openfisca_aotearoa.entities import entities
from openfisca_aotearoa.situation_examples import child_disability_allowance

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class AotearoaLegislationModel(TaxBenefitSystem):
    '''Aotearoa legislation system'''

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)

        param_dir = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_dir)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

        self.cache_blacklist = conf_cache_blacklist

        self.open_api_config = {
            'variable_example': 'social_security__residential_requirement',
            'parameter_example': 'social_security.jobseeker_support.base',
            'simulation_example': child_disability_allowance,
            }
