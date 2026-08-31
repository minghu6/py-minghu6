from numbers import Number
from statistics import StatisticsError, quantiles, median


def winsoring(samples: list[Number], n: int, e: int):
    """ [Winsoring](https://en.wikipedia.org/wiki/Winsorizing) high e/n and low e/n

    in-place
    """

    if not 2 * e < n:
        raise StatisticsError('must satisfy 2 * e < n')

    # percentiles
    pcts = quantiles(samples, n=n)

    lo = pcts[e - 1]
    hi = pcts[n - e - 1]

    for i in range(len(samples)):
        if samples[i] > hi:
            samples[i] = hi

        elif samples[i] < lo:
            samples[i] = lo


def median_abs_dev(samples: list[Number]) -> Number:
    x0 = median(samples)

    return median(list(map(lambda x: abs(x - x0), samples)))


def median_abs_dev_pct(samples: list[Number]) -> Number:
    x0 = median(samples)

    return median(list(map(lambda x: abs(x - x0), samples))) / x0
