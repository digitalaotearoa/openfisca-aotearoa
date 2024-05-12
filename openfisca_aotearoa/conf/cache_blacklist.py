# When using openfisca for a large population, having too many variables in cache make openfisca performances drop.
# The following variables are intermediate results and do not need to be cached in those usecases.

cache_blacklist = set([])