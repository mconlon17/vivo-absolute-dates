"""
    absolute_dates.py -- convert the data store from duplicated dates to
    absolute date time value entities.  All date time values become first
    class objects in VIVO, reusable and invertable.

    Version 0.0 2013-12-03 MC
    --  Complete first draft
    Version 0.1 2014-08-23 MC
    --  Upgrading to current coding practices

    To Do
    Test merge_uri
"""


__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"


from vivofoundation import rdf_header
from vivofoundation import rdf_footer
from vivofoundation import vivo_sparql_query
from vivofoundation import merge_uri
from vivofoundation import make_datetime_rdf
from datetime import datetime, date


def make_multidate_dictionary(datetime_precision="vivo:yearPrecision",
                              debug=False):
    """
    Given a VIVO datetime precision, return a dictionary of the URIs for each
    date value with that precision.  For any date value, this function
    returns a list of the URIs representing dates with the specified date
    value.
    """
    query = """
    SELECT ?uri ?dt
    WHERE {
        ?uri vivo:dateTimePrecision {{datetime_precision}} .
        ?uri a vivo:DateTimeValue .
        ?uri vivo:dateTime ?dt .
    }"""
    query = query.replace("{{datetime_precision}}", datetime_precision)
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except IndexError:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    multidate_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        if datetime_precision == "vivo:yearPrecision":
            dt = b['dt']['value'][0:4]
            dtv = datetime.strptime(dt, '%Y')
        elif datetime_precision == "vivo:yearMonthPrecision":
            dt = b['dt']['value'][0:7]
            dtv = datetime.strptime(dt, '%Y-%m')
        elif datetime_precision == "vivo:yearMonthDayPrecision":
            dt = b['dt']['value'][0:10]
            dtv = datetime.strptime(dt, '%Y-%m-%d')
        uri = b['uri']['value']
        if dtv in multidate_dictionary:
            multidate_dictionary[dtv].append(uri)
        else:
            multidate_dictionary[dtv] = [uri]
        i = i + 1
    return multidate_dictionary


# Set date range to two hundred years from the founding of the university

date_range = [date(1853, 1, 1), date(2053, 12, 31)]
print datetime.now(), "Start"
ardf = rdf_header()
srdf = rdf_header()

# for datetime_precision in ["vivo:yearPrecision", "vivo:yearMonthPrecision",
#                       "vivo:yearMonthDayPrecision"]:
for datetime_precision in ["vivo:yearMonthPrecision"]:
    date_dict = make_multidate_dictionary(datetime_precision, debug=True)

    for dtv in sorted(date_dict.keys()):
        print dtv, len(date_dict[dtv])

    # # Merge all multiple occurrences to single occurrence
    #
    # for date in date_dict.keys():
    #     date_list = date_dict[date]
    #     if len(date_list) > 1:
    #         to_uri = date_list[0]
    #         for from_uri in date_list[1:]:
    #             [add, sub] = merge_uri(from_uri, to_uri)
    #             ardf = ardf + add
    #             srdf = srdf + sub
    #
    # # Fill in the missing dates
    #
    # for date_value in range(date_range, datePrecision):
    #     if date not in date_dict:
    #         add = make_datetime_rdf(date_value, datetime_precision)
    #         ardf = ardf + add

ardf = ardf + rdf_footer()
srdf = srdf + rdf_footer()
print datetime.now(), "Finished"
print ardf
print srdf
