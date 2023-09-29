from numpy.typing import NDArray
from typing import Callable

import dataclasses

import numpy

Vector = NDArray[numpy.float_]


@dataclasses.dataclass
class AbatementRate:
    """Abatement rate applicable to income-tested benefits.

    Income test means that the applicable rate of a benefit must be reduced by
    a certain amount for each unit of income defined by the policy-maker, above
    a certain floor but below a certain ceiling.

    Abatement rate is the application of an income test to a specific benefit,
    taking into account that benefit's own definition of total income; that is,
    "the rate at which a rate of benefit [...] must, under the appropriate
    income test, be reduced on account of income."

    .. see:: https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375

    """

    #: Applicable rate of benefit to be reduced.
    applicable_rate: Vector

    #: Total income of the beneficiary and the beneficiary’s spouse or partner.
    total_income: Vector

    def __call__(self, income_test: Callable[[Vector], Vector]) -> Vector:
        """Apply an income test to a benefit's applicable rate."""
        return income_test(numpy.floor(self.total_income))
