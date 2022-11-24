"""TODO: Add missing doctring."""

from pathlib import Path

import numpy
import pandas

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__part_of_nz(variables.Variable):
    label = "TODO"
    reference = "https://datafinder.stats.govt.nz/layer/27780-urban-area-2017-generalised-version/"
    documentation = """TODO"""
    entity = entities.Person
    value_type = str
    default_value = "Other"
    definition_period = periods.DateUnit.WEEK


class AccommodationSupplement__AreaOfResidence(indexed_enums.Enum):
    unknown = "We have no idea"
    area_1 = "Area 1"
    area_2 = "Area 2"
    area_3 = "Area 3"
    area_4 = "Area 4"


class accommodation_supplement__area_of_residence(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784877"
    documentation = """TODO"""
    entity = entities.Person
    value_type = indexed_enums.Enum
    possible_values = AccommodationSupplement__AreaOfResidence
    default_value = AccommodationSupplement__AreaOfResidence.unknown
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        area_of_residence = AccommodationSupplement__AreaOfResidence
        params_path = "openfisca_aotearoa/parameters"
        file_path = "social_security/accommodation_supplement"
        area_path = Path(f"{params_path}/{file_path}/area.csv").resolve()

        # We read locations from a database.
        part_of_nz = people("accommodation_supplement__part_of_nz", period)
        area_of_nz = pandas.read_csv(area_path, sep = ";")
        name = area_of_nz["UA2017_NAME"]
        area = "SSA2018_AREA"
        locations = (numpy.flatnonzero(name.isin([loc])) for loc in part_of_nz)

        # The we map locations to each area 1-4.
        areas_of_residence = (
            area_of_residence[area_of_nz.at[index[0], area]].index
            if len(index) > 0 else area_of_residence.area_4.index
            for index in locations
            )

        ssa2018_sched_4_part_7_8 = numpy.fromiter(
            areas_of_residence,
            dtype = int,
            )

        # And return the result.
        return ssa2018_sched_4_part_7_8
