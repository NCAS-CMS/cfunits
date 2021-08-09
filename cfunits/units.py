import ctypes
import ctypes.util
import operator

from numpy import array as numpy_array
from numpy import asanyarray as numpy_asanyarray
from numpy import dtype as numpy_dtype
from numpy import generic as numpy_generic
from numpy import ndarray as numpy_ndarray
from numpy import shape as numpy_shape
from numpy import size as numpy_size

# --------------------------------------------------------------------
# Aliases for ctypes
# --------------------------------------------------------------------
_sizeof_buffer = 257
_string_buffer = ctypes.create_string_buffer(_sizeof_buffer)
_c_char_p = ctypes.c_char_p
_c_int = ctypes.c_int
_c_uint = ctypes.c_uint
_c_float = ctypes.c_float
_c_double = ctypes.c_double
_c_size_t = ctypes.c_size_t
_c_void_p = ctypes.c_void_p
_pointer = ctypes.pointer
_POINTER = ctypes.POINTER

_ctypes_POINTER = {4: _POINTER(_c_float), 8: _POINTER(_c_double)}

# --------------------------------------------------------------------
# Load the Udunits-2 library and read the database
# --------------------------------------------------------------------
# if sys.platform == 'darwin':
#     # This has been tested on Mac OSX 10.5.8 and 10.6.8
#     _udunits = ctypes.CDLL('libudunits2.0.dylib')
# else:
#     # Linux
#     _udunits = ctypes.CDLL('libudunits2.so.0')
_libpath = ctypes.util.find_library("udunits2")
if _libpath is None:
    raise FileNotFoundError(
        "cfunits requires UNIDATA UDUNITS-2. Can't find the 'udunits2' "
        "library."
    )

_udunits = ctypes.CDLL(_libpath)

# Suppress "overrides prefixed-unit" messages. This also suppresses
# all other error messages - so watch out!
#
# Messages may be turned back on by calling the module function
# udunits_error_messages.
# ut_error_message_handler ut_set_error_message_handler(
#                                   ut_error_message_handler handler);
_ut_set_error_message_handler = _udunits.ut_set_error_message_handler
_ut_set_error_message_handler.argtypes = (_c_void_p,)
_ut_set_error_message_handler.restype = _c_void_p

_ut_set_error_message_handler(_udunits.ut_ignore)

# Read the data base
# ut_system* ut_read_xml(const char* path);
_ut_read_xml = _udunits.ut_read_xml
_ut_read_xml.argtypes = (_c_char_p,)
_ut_read_xml.restype = _c_void_p

# print('units: before _udunits.ut_read_xml(',_unit_database,')')
_ut_system = _ut_read_xml(None)
# print('units: after  _udunits.ut_read_xml(',_unit_database,')')

# Reinstate the reporting of error messages
# _ut_set_error_message_handler(_udunits.ut_write_to_stderr)

# --------------------------------------------------------------------
# Aliases for the UDUNITS-2 C API. See
# http://www.unidata.ucar.edu/software/udunits/udunits-2.0.4/udunits2lib.html
# for documentation.
# --------------------------------------------------------------------
# int ut_format(const ut_unit* const unit, char* buf, size_t size,
#               unsigned opts);
_ut_format = _udunits.ut_format
_ut_format.argtypes = (_c_void_p, _c_char_p, _c_size_t, _c_uint)
_ut_format.restype = _c_int

# char* ut_trim(char* const string, const ut_encoding encoding);
_ut_trim = _udunits.ut_trim
# ut_encoding assumed to be int!:
_ut_trim.argtypes = (_c_char_p, _c_int)
_ut_trim.restype = _c_char_p

# ut_unit* ut_parse(const ut_system* const system,
#                   const char* const string, const ut_encoding encoding);
_ut_parse = _udunits.ut_parse
# ut_encoding assumed to be int!:
_ut_parse.argtypes = (_c_void_p, _c_char_p, _c_int)
_ut_parse.restype = _c_void_p

# int ut_compare(const ut_unit* const unit1, const ut_unit* const
#                unit2);
_ut_compare = _udunits.ut_compare
_ut_compare.argtypes = (_c_void_p, _c_void_p)
_ut_compare.restype = _c_int

# int ut_are_convertible(const ut_unit* const unit1, const ut_unit*
#                        const unit2);
_ut_are_convertible = _udunits.ut_are_convertible
_ut_are_convertible.argtypes = (_c_void_p, _c_void_p)
_ut_are_convertible.restype = _c_int

# cv_converter* ut_get_converter(ut_unit* const from, ut_unit* const
#                                to);
_ut_get_converter = _udunits.ut_get_converter
_ut_get_converter.argtypes = (_c_void_p, _c_void_p)
_ut_get_converter.restype = _c_void_p

# ut_unit* ut_divide(const ut_unit* const numer, const ut_unit* const
#                    denom);
_ut_divide = _udunits.ut_divide
_ut_divide.argtypes = (_c_void_p, _c_void_p)
_ut_divide.restype = _c_void_p

# ut_unit* ut_get_name(const ut_unit* unit, ut_encoding encoding)
_ut_get_name = _udunits.ut_get_name
_ut_get_name.argtypes = (_c_void_p, _c_int)  # ut_encoding assumed to be int!
_ut_get_name.restype = _c_char_p

# ut_unit* ut_offset(const ut_unit* const unit, const double offset);
_ut_offset = _udunits.ut_offset
_ut_offset.argtypes = (_c_void_p, _c_double)
_ut_offset.restype = _c_void_p

# ut_unit* ut_raise(const ut_unit* const unit, const int power);
_ut_raise = _udunits.ut_raise
_ut_raise.argtypes = (_c_void_p, _c_int)
_ut_raise.restype = _c_void_p

# ut_unit* ut_scale(const double factor, const ut_unit* const unit);
_ut_scale = _udunits.ut_scale
_ut_scale.argtypes = (_c_double, _c_void_p)
_ut_scale.restype = _c_void_p

# ut_unit* ut_multiply(const ut_unit* const unit1, const ut_unit*
#                      const unit2);
_ut_multiply = _udunits.ut_multiply
_ut_multiply.argtypes = (_c_void_p, _c_void_p)
_ut_multiply.restype = _c_void_p

# ut_unit* ut_log(const double base, const ut_unit* const reference);
_ut_log = _udunits.ut_log
_ut_log.argtypes = (_c_double, _c_void_p)
_ut_log.restype = _c_void_p

# ut_unit* ut_root(const ut_unit* const unit, const int root);
_ut_root = _udunits.ut_root
_ut_root.argtypes = (_c_void_p, _c_int)
_ut_root.restype = _c_void_p

# void ut_free_system(ut_system*  system);
_ut_free = _udunits.ut_free
_ut_free.argypes = (_c_void_p,)
_ut_free.restype = None

# float* cv_convert_floats(const cv_converter* converter, const float*
#                          const in, const size_t count, float* out);
_cv_convert_floats = _udunits.cv_convert_floats
_cv_convert_floats.argtypes = (_c_void_p, _c_void_p, _c_size_t, _c_void_p)
_cv_convert_floats.restype = _c_void_p

# double* cv_convert_doubles(const cv_converter* converter, const
#                            double* const in, const size_t count,
#                            double* out);
_cv_convert_doubles = _udunits.cv_convert_doubles
_cv_convert_doubles.argtypes = (_c_void_p, _c_void_p, _c_size_t, _c_void_p)
_cv_convert_doubles.restype = _c_void_p

# double cv_convert_double(const cv_converter* converter, const double
#                          value);
_cv_convert_double = _udunits.cv_convert_double
_cv_convert_double.argtypes = (_c_void_p, _c_double)
_cv_convert_double.restype = _c_double

# void cv_free(cv_converter* const conv);
_cv_free = _udunits.cv_free
_cv_free.argtypes = (_c_void_p,)
_cv_free.restype = None

_UT_ASCII = 0
_UT_NAMES = 4
_UT_DEFINITION = 8

_cv_convert_array = {4: _cv_convert_floats, 8: _cv_convert_doubles}

# Some function definitions necessary for the following
# changes to the unit system.
_ut_get_unit_by_name = _udunits.ut_get_unit_by_name
_ut_get_unit_by_name.argtypes = (_c_void_p, _c_char_p)
_ut_get_unit_by_name.restype = _c_void_p
_ut_get_status = _udunits.ut_get_status
_ut_get_status.restype = _c_int
_ut_unmap_symbol_to_unit = _udunits.ut_unmap_symbol_to_unit
_ut_unmap_symbol_to_unit.argtypes = (_c_void_p, _c_char_p, _c_int)
_ut_unmap_symbol_to_unit.restype = _c_int
_ut_map_symbol_to_unit = _udunits.ut_map_symbol_to_unit
_ut_map_symbol_to_unit.argtypes = (_c_char_p, _c_int, _c_void_p)
_ut_map_symbol_to_unit.restype = _c_int
_ut_map_unit_to_symbol = _udunits.ut_map_unit_to_symbol
_ut_map_unit_to_symbol.argtypes = (_c_void_p, _c_char_p, _c_int)
_ut_map_unit_to_symbol.restype = _c_int
_ut_map_name_to_unit = _udunits.ut_map_name_to_unit
_ut_map_name_to_unit.argtypes = (_c_char_p, _c_int, _c_void_p)
_ut_map_name_to_unit.restype = _c_int
_ut_map_unit_to_name = _udunits.ut_map_unit_to_name
_ut_map_unit_to_name.argtypes = (_c_void_p, _c_char_p, _c_int)
_ut_map_unit_to_name.restype = _c_int
_ut_new_base_unit = _udunits.ut_new_base_unit
_ut_new_base_unit.argtypes = (_c_void_p,)
_ut_new_base_unit.restype = _c_void_p

# Change Sv mapping. Both sievert and sverdrup are just aliases,
# so no unit to symbol mapping needs to be changed.
# We don't need to remove rem, since it was constructed with
# the correct sievert mapping in place; because that mapping
# was only an alias, the unit now doesn't depend on the mapping
# persisting.
assert 0 == _ut_unmap_symbol_to_unit(_ut_system, _c_char_p(b"Sv"), _UT_ASCII)
assert 0 == _ut_map_symbol_to_unit(
    _c_char_p(b"Sv"),
    _UT_ASCII,
    _ut_get_unit_by_name(_ut_system, _c_char_p(b"sverdrup")),
)

# Add new base unit calendar_year
calendar_year_unit = _ut_new_base_unit(_ut_system)
assert 0 == _ut_map_symbol_to_unit(
    _c_char_p(b"cY"), _UT_ASCII, calendar_year_unit
)
assert 0 == _ut_map_unit_to_symbol(
    calendar_year_unit, _c_char_p(b"cY"), _UT_ASCII
)
assert 0 == _ut_map_name_to_unit(
    _c_char_p(b"calendar_year"), _UT_ASCII, calendar_year_unit
)
assert 0 == _ut_map_unit_to_name(
    calendar_year_unit, _c_char_p(b"calendar_year"), _UT_ASCII
)
assert 0 == _ut_map_name_to_unit(
    _c_char_p(b"calendar_years"), _UT_ASCII, calendar_year_unit
)


def add_unit_alias(definition, symbol, singular, plural):
    """Registers an alias for an existing unit or value."""
    unit = _ut_parse(
        _ut_system, _c_char_p(definition.encode("utf-8")), _UT_ASCII
    )
    if symbol is not None:
        assert 0 == _ut_map_symbol_to_unit(
            _c_char_p(symbol.encode("utf-8")), _UT_ASCII, unit
        )
    if singular is not None:
        assert 0 == _ut_map_name_to_unit(
            _c_char_p(singular.encode("utf-8")), _UT_ASCII, unit
        )
    if plural is not None:
        assert 0 == _ut_map_name_to_unit(
            _c_char_p(plural.encode("utf-8")), _UT_ASCII, unit
        )


# Add various aliases useful for CF
add_unit_alias(
    "1.e-3", "psu", "practical_salinity_unit", "practical_salinity_units"
)
add_unit_alias("calendar_year/12", "cM", "calendar_month", "calendar_months")
add_unit_alias("1", None, "level", "levels")
add_unit_alias("1", None, "layer", "layers")
add_unit_alias("1", None, "sigma_level", "sigma_levels")
add_unit_alias("1", "dB", "decibel", "debicels")
add_unit_alias("10 dB", None, "bel", "bels")

# _udunits.ut_get_unit_by_name(_udunits.ut_new_base_unit(_ut_system),
#                              _ut_system, 'calendar_year')

# --------------------------------------------------------------------
# Create a calendar year unit
# --------------------------------------------------------------------
# _udunits.ut_map_name_to_unit('calendar_year', _UT_ASCII,
#                              _udunits.ut_new_base_unit(_ut_system))

from cftime import _dateparse as cftime_dateparse
from cftime import datetime as cftime_datetime

_cached_ut_unit = {}
_cached_utime = {}

# --------------------------------------------------------------------
# Save some useful units
# --------------------------------------------------------------------
# A time ut_unit (equivalent to 'day', 'second', etc.)
_day_ut_unit = _ut_parse(_ut_system, _c_char_p(b"day"), _UT_ASCII)
_cached_ut_unit["days"] = _day_ut_unit
# A pressure ut_unit (equivalent to 'Pa', 'hPa', etc.)
_pressure_ut_unit = _ut_parse(_ut_system, _c_char_p(b"pascal"), _UT_ASCII)
_cached_ut_unit["pascal"] = _pressure_ut_unit
# A calendar time ut_unit (equivalent to 'cY', 'cM')
_calendartime_ut_unit = _ut_parse(
    _ut_system, _c_char_p(b"calendar_year"), _UT_ASCII
)
_cached_ut_unit["calendar_year"] = _calendartime_ut_unit
# A dimensionless unit one (equivalent to '', '1', '2', etc.)
# _dimensionless_unit_one = _udunits.ut_get_dimensionless_unit_one(_ut_system)
# _cached_ut_unit['']  = _dimensionless_unit_one
# _cached_ut_unit['1'] = _dimensionless_unit_one

_dimensionless_unit_one = _ut_parse(_ut_system, _c_char_p(b"1"), _UT_ASCII)
_cached_ut_unit[""] = _dimensionless_unit_one
_cached_ut_unit["1"] = _dimensionless_unit_one

# --------------------------------------------------------------------
# Set the default calendar type according to the CF conventions
# --------------------------------------------------------------------
_default_calendar = "gregorian"
_canonical_calendar = {
    "gregorian": "gregorian",
    "standard": "gregorian",
    "none": "gregorian",
    "proleptic_gregorian": "proleptic_gregorian",
    "360_day": "360_day",
    "noleap": "365_day",
    "365_day": "365_day",
    "all_leap": "366_day",
    "366_day": "366_day",
    "julian": "julian",
}

_months_or_years = ("month", "months", "year", "years", "yr")

# # --------------------------------------------------------------------
# # Set month lengths in days for non-leap years (_days_in_month[0,1:])
# # and leap years (_days_in_month[1,1:])
# # --------------------------------------------------------------------
# _days_in_month = numpy_array(
#     [[-99, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
#      [-99, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]])


# --------------------------------------------------------------------
# Function to control Udunits error messages
# --------------------------------------------------------------------
def udunits_error_messages(flag):
    """Controls the printing of error messages from Udunits.

    Error messages are turned off by default in Udunits.

    :Parameters:

        flag: `bool`
            Set to True to print Udunits error messages and False to
            not print Udunits error messages.

    :Returns:

        `None`

    **Examples:**

    >>> udunits_error_messages(True)
    >>> udunits_error_messages(False)

    """
    if flag:
        _ut_set_error_message_handler(_udunits.ut_write_to_stderr)
    else:
        _ut_set_error_message_handler(_udunits.ut_ignore)


# def _month_length(year, month, calendar, _days_in_month=_days_in_month):
#     '''
#
# Find month lengths in days for each year/month pairing in the input
# numpy arrays 'year' and 'month', both of which must have the same
# shape. 'calendar' must be one of the standard CF calendar types.
#
# :Parameters:
#
#
#     '''
#     shape = month.shape
#     if calendar in ('standard', 'gregorian'):
#         leap = numpy_where(year % 4 == 0, 1, 0)
#         leap = numpy_where((year > 1582) &
#                            (year % 100 == 0) & (year % 400 != 0),
#                            0, leap)
#     elif calendar == '360_day':
#         days_in_month = numpy_empty(shape)
#         days_in_month.fill(30)
#         return days_in_month
#
#     elif calendar in ('all_leap', '366_day'):
#         leap = numpy_zeros(shape)
#
#     elif calendar in ('no_leap', '365_day'):
#         leap = numpy_ones(shape)
#
#     elif calendar == 'proleptic_gregorian':
#         leap = numpy_where(year % 4 == 0, 1, 0)
#         leap = numpy_where((year % 100 == 0) & (year % 400 != 0),
#                            0, leap)
#
#     days_in_month = numpy_array([_days_in_month[l, m]
#                                  for l, m in zip(leap.flat, month.flat)])
#     days_in_month.resize(shape)
#
#     return days_in_month
#
# def _proper_date(year, month, day, calendar, fix=False,
#                  _days_in_month=_days_in_month):
#     '''
#
# Given equally shaped numpy arrays of 'year', 'month', 'day' adjust
# them *in place* to be proper dates. 'calendar' must be one of the
# standard CF calendar types.
#
# Excessive number of months are converted to years but excessive days
# are not converted to months nor years. If a day is illegal in the
# proper date then a ValueError is raised, unless 'fix' is True, in
# which case the day is lowered to the nearest legal date:
#
#     2000/26/1 -> 2002/3/1
#
#     2001/2/31 -> ValueError if 'fix' is False
#     2001/2/31 -> 2001/2/28  if 'fix' is True
#     2001/2/99 -> 2001/2/28  if 'fix' is True
#
# :Parameters:
#
#     '''
#     # y, month = divmod(month, 12)
#     # year += y
#
#     year      += month // 12
#     month[...] = month % 12
#
#     mask       = (month == 0)
#     year[...]  = numpy_where(mask, year-1, year)
#     month[...] = numpy_where(mask, 12, month)
#     del mask
#
#     days_in_month = _month_length(year, month, calendar,
#                                   _days_in_month=_days_in_month)
#
#     if fix:
#         day[...] = numpy_where(day > days_in_month, days_in_month, day)
#     elif (day > days_in_month).any():
#         raise ValueError("Illegal date(s) in %s calendar" % calendar)
#
#     return year, month, day


# --------------------------------------------------------------------
# Constants, as defined by UDUNITS
# --------------------------------------------------------------------
_year_length = 365.242198781
_month_length = _year_length / 12


class Units:
    """Utilities for working with physical units.

    Store, combine and compare physical units and convert numeric
    values to different units.

    Units are as defined in UNIDATA's Udunits-2 package, with a few
    exceptions for greater consistency with the CF conventions namely
    support for CF calendars and new units definitions.


    **Modifications to the standard Udunits database**

    Whilst a standard Udunits-2 database may be used, greater
    consistency with CF is achieved by using a modified database. The
    following units are either new to, modified from, or removed from
    the standard Udunits-2 database (version 2.1.24):

    =======================  ======  ============  ==============
    Unit name                Symbol  Definition    Status
    =======================  ======  ============  ==============
    practical_salinity_unit  psu     1e-3          New unit
    level                            1             New unit
    sigma_level                      1             New unit
    layer                            1             New unit
    decibel                  dB      1             New unit
    bel                              10 dB         New unit
    sverdrup                 Sv      1e6 m3 s-1    Added symbol
    sievert                          J kg-1        Removed symbol
    =======================  ======  ============  ==============

    Plural forms of the new units' names are allowed, such as
    ``practical_salinity_units``.

    The modified database is in the *udunits* subdirectory of the
    *etc* directory found in the same location as this module.


    **Accessing units**

    Units may be set, retrieved and deleted via the `units`
    attribute. Its value is a string that can be recognized by
    UNIDATA's Udunits-2 package, with the few exceptions given in the
    CF conventions.

    >>> u = Units('m s-1')
    >>> u
    <Units: m s-1>
    >>> v = Units('days since 2004-3-1')
    >>> v
    <Units: days since 2004-3-1>


    **Equality and equivalence of units**

    There are methods for assessing whether two units are equivalent
    or equal. Two units are equivalent if numeric values in one unit
    are convertible to numeric values in the other unit (such as
    ``kilometres`` and ``metres``). Two units are equal if they are
    equivalent and their conversion is a scale factor of 1 and an
    offset of 0 (such as ``kilometres`` and ``1000 metres``). Note
    that equivalence and equality are based on internally stored
    binary representations of the units, rather than their string
    representations.

    >>> u = Units('m/s')
    >>> v = Units('m s-1')
    >>> w = Units('km.s-1')
    >>> x = Units('0.001 kilometer.second-1')
    >>> y = Units('gram')

    >>> u.equivalent(v), u.equals(v),  u == v
    (True, True, True)
    >>> u.equivalent(w), u.equals(w)
    (True, False)
    >>> u.equivalent(x), u.equals(x)
    (True, True)
    >>> u.equivalent(y), u.equals(y)
    (False, False)


    **Time and reference time units**

    Time units may be given as durations of time (*time units*) or as
    an amount of time since a reference time (*reference time units*):

    >>> v = Units()
    >>> v = Units('s')
    >>> v = Units('day')
    >>> v = Units('days since 1970-01-01')
    >>> v = Units('seconds since 1992-10-8 15:15:42.5 -6:00')

    .. note:: It is recommended that the units ``year`` and ``month``
              be used with caution, as explained in the following
              excerpt from the CF conventions: "The Udunits package
              defines a year to be exactly 365.242198781 days (the
              interval between 2 successive passages of the sun
              through vernal equinox). It is not a calendar
              year. Udunits includes the following definitions for
              years: a common_year is 365 days, a leap_year is 366
              days, a Julian_year is 365.25 days, and a Gregorian_year
              is 365.2425 days. For similar reasons the unit
              ``month``, which is defined to be exactly year/12,
              should also be used with caution."

    **Calendar**

    The date given in reference time units is associated with one of
    the calendars recognized by the CF conventions and may be set with
    the `calendar` attribute. However, as in the CF conventions, if
    the calendar is not set then, for the purposes of calculation and
    comparison, it defaults to the mixed Gregorian/Julian calendar as
    defined by Udunits:

    >>> u = Units('days since 2000-1-1')
    >>> u.calendar
    Traceback (most recent call last):
        ...
    AttributeError: Units has no attribute 'calendar'
    >>> v = Units('days since 2000-1-1', 'gregorian')
    >>> v.calendar
    'gregorian'
    >>> v.equals(u)
    True


    **Arithmetic with units**

    The following operators, operations and assignments are
    overloaded:

    Comparison operators:

        ``==, !=, >, >=, <, <=``

    Binary arithmetic operations:

        ``+, -, *, /, //, pow(), **, %``

    Unary arithmetic operations:

        ``-, +``

    Augmented arithmetic assignments:

        ``+=, -=, *=, /=, //=, **=``

    The comparison operations return a boolean and all other
    operations return a new units object or modify the units object in
    place.

    >>> u = Units('m')
    >>> u
    <Units: m>

    >>> v = u * 1000
    >>> v
    <Units: 1000 m>

    >>> u == v
    False
    >>> u != v
    True

    >>> u **= 2
    >>> u
    <Units: m2>

    It is also possible to create the logarithm of a unit
    corresponding to the given logarithmic base:

    >>> u = Units('seconds')
    >>> u.log(10)
    <Units: lg(re 1 s)>


    **Modifying data for equivalent units**

    Any numpy array or Python numeric type may be modified for
    equivalent units using the `conform` static method.

    >>> Units.conform(2, Units('km'), Units('m'))
    2000.0

    >>> import numpy
    >>> a = numpy.arange(5.0)
    >>> Units.conform(a, Units('minute'), Units('second'))
    array([   0.,   60.,  120.,  180.,  240.])
    >>> a
    array([0., 1., 2., 3., 4.])

    If the *inplace* keyword is True, then a numpy array is modified
    in place, without any copying overheads:

    >>> Units.conform(
    ...     a,
    ...     Units('days since 2000-12-1'),
    ...     Units('days since 2001-1-1'),
    ...     inplace=True
    ... )
    array([-31., -30., -29., -28., -27.])
    >>> a
    array([-31., -30., -29., -28., -27.])

    """

    def __init__(
        self,
        units=None,
        calendar=None,
        formatted=False,
        names=False,
        definition=False,
        _ut_unit=None,
    ):
        """Initialises the `Units` instance.

        :Parameters:

            units: `str` or `Units`, optional
                Set the new units from this string.

            calendar: `str`, optional
                Set the calendar for reference time units.

            formatted: `bool`, optional
                Format the string representation of the units in a
                standardized manner. See the `formatted` method.

            names: `bool`, optional
                Format the string representation of the units using names
                instead of symbols. See the `formatted` method.

            definition: `bool`, optional
                Format the string representation of the units using basic
                units. See the `formatted` method.

            _ut_unit: `int`, optional
                Set the new units from this Udunits binary unit
                representation. This should be an integer returned by a
                call to `ut_parse` function of Udunits. Ignored if *units*
                is set.

        """
        if isinstance(units, self.__class__):
            self.__dict__ = units.__dict__
            return

        self._isvalid = True
        self._reason_notvalid = ""
        self._units = units
        self._ut_unit = None
        self._isreftime = False
        self._calendar = calendar
        self._canonical_calendar = None
        self._utime = None
        self._units_since_reftime = None

        # Set the calendar
        _calendar = None
        if calendar is not None:
            _calendar = _canonical_calendar.get(calendar.lower())
            if _calendar is None:
                self._new_reason_notvalid(f"Invalid calendar={calendar!r}")
                self._isvalid = False
                _calendar = calendar

        if units is not None:
            try:
                units = units.strip()
            except AttributeError:
                self._isvalid = False
                self._new_reason_notvalid(f"Bad units type: {type(units)}")
                return

            unit = None

            if isinstance(units, str) and " since " in units:
                # ----------------------------------------------------
                # Set a reference time unit
                # ----------------------------------------------------
                # Set the calendar
                if calendar is None:
                    _calendar = _default_calendar
                else:
                    _calendar = _canonical_calendar.get(calendar.lower())
                    if _calendar is None:
                        _calendar = calendar

                units_split = units.split(" since ")
                unit = units_split[0].strip()

                self._units_since_reftime = unit

                ut_unit = _cached_ut_unit.get(unit, None)
                if ut_unit is None:
                    ut_unit = _ut_parse(
                        _ut_system, _c_char_p(unit.encode("utf-8")), _UT_ASCII
                    )
                    if not ut_unit or not _ut_are_convertible(
                        ut_unit, _day_ut_unit
                    ):
                        ut_unit = None
                        self._isvalid = False
                    else:
                        _cached_ut_unit[unit] = ut_unit

                if (_calendar, units) in _cached_utime:
                    utime = _cached_utime[(_calendar, units)]
                else:
                    unit_string = f"{unit} since {units_split[1].strip()}"
                    utime = _cached_utime.get((_calendar, unit_string))
                    if utime is None:
                        try:
                            d = cftime_dateparse(
                                unit_string, calendar=_calendar
                            )
                        except Exception as error:
                            self._new_reason_notvalid(str(error))
                            self._isvalid = False
                        else:
                            utime = cftime_datetime(
                                *d.timetuple()[:6], calendar=_calendar
                            )
                            _cached_utime[(_calendar, unit_string)] = utime

                self._isreftime = True
                self._calendar = calendar
                self._canonical_calendar = _calendar
                self._utime = utime

            else:
                # ----------------------------------------------------
                # Set a unit other than a reference time unit
                # ----------------------------------------------------
                ut_unit = _cached_ut_unit.get(units, None)
                if ut_unit is None:
                    ut_unit = _ut_parse(
                        _ut_system, _c_char_p(units.encode("utf-8")), _UT_ASCII
                    )
                    if not ut_unit:
                        ut_unit = None
                        self._isvalid = False
                        self._new_reason_notvalid(
                            f"Invalid units: {units!r}; Not recognised by "
                            "UDUNITS"
                        )
                    else:
                        _cached_ut_unit[units] = ut_unit

                self._isreftime = False
                self._calendar = None
                self._canonial_calendar = None
                self._utime = None

            self._ut_unit = ut_unit
            self._units = units
            self._units_since_reftime = unit

            if formatted or names or definition:
                self._units = self.formatted(names, definition)

            return

        elif calendar:
            # ---------------------------------------------------------
            # Calendar is set, but units are not.
            # ---------------------------------------------------------
            self._units = None
            self._ut_unit = None
            self._isreftime = True
            self._calendar = calendar
            self._canonical_calendar = _canonical_calendar[calendar.lower()]
            self._units_since_reftime = None

            return

        if _ut_unit is not None:
            # ---------------------------------------------------------
            # _ut_unit is set
            # ---------------------------------------------------------
            self._ut_unit = _ut_unit
            self._isreftime = False

            units = self.formatted(names, definition)
            _cached_ut_unit[units] = _ut_unit
            self._units = units

            self._units_since_reftime = None

            self._calendar = None
            self._utime = None

            return

        # -------------------------------------------------------------
        # Nothing has been set
        # -------------------------------------------------------------
        self._units = None
        self._ut_unit = None
        self._isreftime = False
        self._calendar = None
        self._canonical_calendar = None
        self._utime = None
        self._units_since_reftime = None

    def __getstate__(self):
        """Called when pickling.

        :Returns:

            `dict`
                A dictionary of the instance's attributes

        **Examples:**

        >>> u = Units('days since 3-4-5', calendar='gregorian')
        >>> u.__getstate__()
        {'_units': 'days since 3-4-5',
         '_calendar': 'gregorian'}

        """
        return dict(
            [
                (attr, getattr(self, attr))
                for attr in ("_units", "_calendar")
                if hasattr(self, attr)
            ]
        )

    def __setstate__(self, odict):
        """Called when unpickling.

        :Parameters:

            odict: `dict`
                The output from the instance's `__getstate__` method.

        :Returns:

            `None`

        """
        units = None
        if "_units" in odict:
            units = odict["_units"]

        calendar = None
        if "_calendar" in odict:
            calendar = odict["_calendar"]

        self.__init__(units=units, calendar=calendar)

    def __hash__(self):
        """Returns an integer representation of the `Units` object.

        x.__hash__() is logically equivalent to hash(x)

        """
        if not self._isreftime:
            return hash(("Units", self._ut_unit))

        #        origin = self._utime.origin
        origin = self._utime

        return hash(
            ("Units", self._ut_unit, origin)  # , self._utime.calendar)
        )

    def __repr__(self):
        """Returns a printable representation of the `Units` object.

        x.__repr__() is logically equivalent to repr(x)

        """
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        """Returns a string version of the `Units` object.

        x.__str__() is logically equivalent to str(x)

        """
        string = []
        if self._units is not None:
            if self._units == "":
                string.append("''")
            else:
                string.append(str(self._units))

        if self._calendar is not None:
            string.append(f"{self._calendar}")

        return " ".join(string)

    def __deepcopy__(self, memo):
        """Used if copy.deepcopy is called on the variable."""
        return self

    def __bool__(self):
        """Truth value testing and the built-in operation ``bool``.

        x.__bool__() is logically equivalent to x!=0

        """
        return self._ut_unit is not None

    def __eq__(self, other):
        """The rich comparison operator ``==``.

        x.__eq__(y) is logically equivalent to x==y

        """
        return self.equals(other)

    def __ne__(self, other):
        """The rich comparison operator ``!=``.

        x.__ne__(y) is logically equivalent to x!=y

        """
        return not self.equals(other)

    def __gt__(self, other):
        """The rich comparison operator ``>``.

        x.__gt__(y) is logically equivalent to x>y

        """
        return self._comparison(other, "__gt__")

    def __ge__(self, other):
        """The rich comparison operator ``>=``.

        x.__ge__(y) is logically equivalent to x>=y

        """
        return self._comparison(other, "__ge__")

    def __lt__(self, other):
        """The rich comparison operator ``<``.

        x.__lt__(y) is logically equivalent to x<y

        """
        return self._comparison(other, "__lt__")

    def __le__(self, other):
        """The rich comparison operator ``<=``.

        x.__le__(y) is logically equivalent to x<=y

        """
        return self._comparison(other, "__le__")

    def __sub__(self, other):
        """The binary arithmetic operation ``-``.

        x.__sub__(y) is logically equivalent to x-y

        """
        value_error = ValueError(f"Can't do {self!r} - {other!r}")

        if self._isreftime or (
            isinstance(other, self.__class__) and other._isreftime
        ):
            raise value_error

        try:
            _ut_unit = _ut_offset(self._ut_unit, _c_double(other))
            return type(self)(_ut_unit=_ut_unit)
        except:
            raise value_error

    def __add__(self, other):
        """The binary arithmetic operation ``+``.

        x.__add__(y) is logically equivalent to x+y

        """
        value_error = ValueError(f"Can't do {self!r} + {other!r}")

        if self._isreftime or (
            isinstance(other, self.__class__) and other._isreftime
        ):
            raise value_error

        try:
            _ut_unit = _ut_offset(self._ut_unit, _c_double(-other))
            return type(self)(_ut_unit=_ut_unit)
        except:
            raise value_error

    def __mul__(self, other):
        """The binary arithmetic operation ``*``.

        x.__mul__(y) is logically equivalent to x*y

        """
        value_error = ValueError(f"Can't do {self!r} * {other!r}")

        if isinstance(other, self.__class__):
            if self._isreftime or other._isreftime:
                raise value_error

            try:
                ut_unit = _ut_multiply(self._ut_unit, other._ut_unit)
            except:
                raise value_error
        else:
            if self._isreftime:
                raise value_error

            try:
                ut_unit = _ut_scale(_c_double(other), self._ut_unit)
            except:
                raise value_error

        return type(self)(_ut_unit=ut_unit)

    def __div__(self, other):
        """The binary arithmetic operation ``/``.

        x.__div__(y) is logically equivalent to x/y

        """
        value_error = ValueError(f"Can't do {self!r} / {other!r}")

        if isinstance(other, self.__class__):
            if self._isreftime or other._isreftime:
                raise value_error

            try:
                ut_unit = _ut_divide(self._ut_unit, other._ut_unit)
            except:
                raise value_error
        else:
            if self._isreftime:
                raise value_error

            try:
                ut_unit = _ut_scale(_c_double(1.0 / other), self._ut_unit)
            except:
                raise value_error

        return type(self)(_ut_unit=ut_unit)

    def __pow__(self, other, modulo=None):
        """The binary arithmetic operations ``**`` and ``pow``.

        x.__pow__(y) is logically equivalent to x**y

        """
        # ------------------------------------------------------------
        # y must be either an integer or the reciprocal of a positive
        # integer.
        # ------------------------------------------------------------

        if modulo is not None:
            raise NotImplementedError(
                "3-argument power not supported for "
                f"{self.__class__.__name__!r}"
            )

        if self and not self._isreftime:
            ut_unit = self._ut_unit
            try:
                return type(self)(_ut_unit=_ut_raise(ut_unit, _c_int(other)))
            except:
                pass

            if 0 < other <= 1:
                # If other is a float and (1/other) is a positive
                # integer then take the (1/other)-th root. E.g. if
                # other is 0.125 then we take the 8-th root.
                try:
                    recip_other = 1 / other
                    root = int(recip_other)
                    if recip_other == root:
                        ut_unit = _ut_root(ut_unit, _c_int(root))
                        if ut_unit is not None:
                            return type(self)(_ut_unit=ut_unit)
                except:
                    pass
            else:
                # If other is a float equal to its integer then raise
                # to the integer part. E.g. if other is 3.0 then we
                # raise to the power of 3; if other is -2.0 then we
                # raise to the power of -2
                try:
                    root = int(other)
                    if other == root:
                        ut_unit = _ut_raise(ut_unit, _c_int(root))
                        if ut_unit is not None:
                            return type(self)(_ut_unit=ut_unit)
                except:
                    pass

        raise ValueError(f"Can't do {self!r} ** {other!r}")

    def __isub__(self, other):
        """The augmented arithmetic assignment ``-=``.

        x.__isub__(y) is logically equivalent to x-=y

        """
        return self - other

    def __iadd__(self, other):
        """The augmented arithmetic assignment ``+=``.

        x.__iadd__(y) is logically equivalent to x+=y

        """
        return self + other

    def __imul__(self, other):
        """The augmented arithmetic assignment ``*=``.

        x.__imul__(y) is logically equivalent to x*=y

        """
        return self * other

    def __idiv__(self, other):
        """The augmented arithmetic assignment ``/=``.

        x.__idiv__(y) is logically equivalent to x/=y

        """
        return self / other

    def __ipow__(self, other):
        """The augmented arithmetic assignment ``**=``.

        x.__ipow__(y) is logically equivalent to x**=y

        """
        return self ** other

    def __rsub__(self, other):
        """Binary arithmetic operation ``-`` with reflected operands.

        x.__rsub__(y) is logically equivalent to y-x

        """
        try:
            return -self + other
        except:
            raise ValueError(f"Can't do {other!r} - {self!r}")

    def __radd__(self, other):
        """Binary arithmetic operation ``+`` with reflected operands.

        x.__radd__(y) is logically equivalent to y+x

        """
        return self + other

    def __rmul__(self, other):
        """Binary arithmetic operation ``*`` with reflected operands.

        x.__rmul__(y) is logically equivalent to y*x

        """
        return self * other

    def __rdiv__(self, other):
        """Binary arithmetic operation ``/`` with reflected operands.

        x.__rdiv__(y) is logically equivalent to y/x

        """
        try:
            return (self ** -1) * other
        except:
            raise ValueError(f"Can't do {other!r} / {self!r}")

    def __floordiv__(self, other):
        """The binary arithmetic operation ``//``.

        x.__floordiv__(y) is logically equivalent to x//y and to x/y

        """
        return self / other

    def __ifloordiv__(self, other):
        """The augmented arithmetic assignment ``//=``.

        x.__ifloordiv__(y) is logically equivalent to x//=y and to x/=y

        """
        return self / other

    def __rfloordiv__(self, other):
        """Binary arithmetic operation ``//`` with reflected operands.

        x.__rfloordiv__(y) is logically equivalent to y//x and to y/x

        """
        try:
            return (self ** -1) * other
        except:
            raise ValueError(f"Can't do {other!r} // {self!r}")

    def __truediv__(self, other):
        """The binary arithmetic operation ``/``.

        x.__truediv__(y) is logically equivalent to x/y

        """
        return self.__div__(other)

    def __itruediv__(self, other):
        """The augmented arithmetic assignment ``/=``.

        x.__itruediv__(y) is logically equivalent to x/=y

        """
        return self.__idiv__(other)

    def __rtruediv__(self, other):
        """Binary arithmetic operation ``/`` with reflected operands.

        x.__rtruediv__(y) is logically equivalent to y/x

        """
        return self.__rdiv__(other)

    def __mod__(self, other):
        """The binary arithmetic operation ``%``.

        x.__mod__(y) is logically equivalent to y%x

        """
        raise ValueError(f"Can't do {other!r} % {self!r}")

    def __neg__(self):
        """The unary arithmetic operation ``-``.

        x.__neg__() is logically equivalent to -x

        """
        return self * -1

    def __pos__(self):
        """The unary arithmetic operation ``+``.

        x.__pos__() is logically equivalent to +x.

        """
        return self

    # ----------------------------------------------------------------
    # Private methods
    # ----------------------------------------------------------------
    def _comparison(self, other, method):
        """Compares two units according to a specified method."""
        value_error = ValueError(
            f"Units are not compatible: {self!r}, {other!r}"
        )
        try:
            cv_converter = _ut_get_converter(self._ut_unit, other._ut_unit)
        except:
            raise value_error

        if not cv_converter:
            _cv_free(cv_converter)
            raise value_error

        y = _c_double(1.0)
        pointer = ctypes.pointer(y)
        _cv_convert_doubles(cv_converter, pointer, _c_size_t(1), pointer)
        _cv_free(cv_converter)

        return getattr(operator, method)(y.value, 1)

    def _new_reason_notvalid(self, reason):
        """Registers a reason that a Units object is not valid."""
        _reason_notvalid = self._reason_notvalid
        if _reason_notvalid:
            self._reason_notvalid = _reason_notvalid + "; " + reason
        else:
            self._reason_notvalid = reason

    # ----------------------------------------------------------------
    # Attributes
    # ----------------------------------------------------------------
    @property
    def has_offset(self):
        """True if the units contain an offset.

        Note that if a multiplicative component of the units had an offset
        during instantiation, then the offset is ignored in the resulting
        `Units` object. See below for examples.

        **Examples**

        >>> Units('K').has_offset
        False
        >>> Units('K @ 0').has_offset
        False
        >>> Units('K @ 273.15').has_offset
        True
        >>> Units('degC').has_offset
        True
        >>> Units('degF').has_offset
        True

        >>> Units('Watt').has_offset
        False
        >>> Units('m2.kg.s-3').has_offset
        False

        >>> Units('km').has_offset
        False
        >>> Units('1000 m').has_offset
        False

        >>> Units('m2.kg.s-3 @ 3.14').has_offset
        True
        >>> Units('(K @ 273.15) m s-1').has_offset
        False
        >>> Units('degC m s-1').has_offset
        False
        >>> Units('degC m s-1') == Units('K m s-1')
        True

        """
        return "@" in self.formatted()

    @property
    def isreftime(self):
        """True if the units are reference time units, false otherwise.

        Note that time units (such as ``'days'``) are not reference time
        units.

        .. seealso:: `isdimensionless`, `islongitude`, `islatitude`,
                     `ispressure`, `istime`

        **Examples:**

        >>> Units('days since 2000-12-1 03:00').isreftime
        True
        >>> Units('hours since 2100-1-1', calendar='noleap').isreftime
        True
        >>> Units(calendar='360_day').isreftime
        True
        >>> Units('days').isreftime
        False
        >>> Units('kg').isreftime
        False
        >>> Units().isreftime
        False

        """
        return self._isreftime

    @property
    def iscalendartime(self):
        """True if the units are calendar time units, false otherwise.

        Note that regular time units (such as ``'days'``) are not calendar
        time units.

        .. seealso:: `isdimensionless`, `islongitude`, `islatitude`,
                     `ispressure`, `isreftime`, `istime`

        **Examples:**

        >>> Units('calendar_months').iscalendartime
        True
        >>> Units('calendar_years').iscalendartime
        True
        >>> Units('days').iscalendartime
        False
        >>> Units('km s-1').iscalendartime
        False
        >>> Units('kg').isreftime
        False
        >>> Units('').isreftime
        False
        >>> Units().isreftime
        False

        """
        return bool(_ut_are_convertible(self._ut_unit, _calendartime_ut_unit))

    @property
    def isdimensionless(self):
        """True if the units are dimensionless, false otherwise.

        .. seealso:: `islongitude`, `islatitude`, `ispressure`, `isreftime`,
                     `istime`

        **Examples:**

        >>> Units('').isdimensionless
        True
        >>> Units('1').isdimensionless
        True
        >>> Units('100').isdimensionless
        True
        >>> Units('m/m').isdimensionless
        True
        >>> Units('m km-1').isdimensionless
        True
        >>> Units().isdimensionless
        False
        >>> Units('m').isdimensionless
        False
        >>> Units('m/s').isdimensionless
        False
        >>> Units('days since 2000-1-1', calendar='noleap').isdimensionless
        False

        """
        return bool(
            _ut_are_convertible(self._ut_unit, _dimensionless_unit_one)
        )

    @property
    def ispressure(self):
        """True if the units are pressure units, false otherwise.

        .. seealso:: `isdimensionless`, `islongitude`, `islatitude`,
                     `isreftime`, `istime`

        **Examples:**

        >>> Units('bar').ispressure
        True
        >>> Units('hPa').ispressure
        True
        >>> Units('meter^-1-kilogram-second^-2').ispressure
        True
        >>> Units('hours since 2100-1-1', calendar='noleap').ispressure
        False

        """
        ut_unit = self._ut_unit
        if ut_unit is None:
            return False

        return bool(_ut_are_convertible(ut_unit, _pressure_ut_unit))

    @property
    def islatitude(self):
        """True if and only if the units are latitude units.

        This is the case if and only if the `units` attribute is one of
        ``'degrees_north'``, ``'degree_north'``, ``'degree_N'``,
        ``'degrees_N'``, ``'degreeN'``, and ``'degreesN'``.

        Note that units of ``'degrees'`` are not latitude units.

        .. seealso:: `isdimensionless`, `islongitude`, `ispressure`,
                     `isreftime`, `istime`

        **Examples:**

        >>> Units('degrees_north').islatitude
        True
        >>> Units('degrees').islatitude
        False
        >>> Units('degrees_east').islatitude
        False
        >>> Units('kg').islatitude
        False
        >>> Units().islatitude
        False

        """
        return self._units in (
            "degrees_north",
            "degree_north",
            "degree_N",
            "degrees_N",
            "degreeN",
            "degreesN",
        )

    @property
    def islongitude(self):
        """True if and only if the units are longitude units.

        This is the case if and only if the `units` attribute is one of
        ``'degrees_east'``, ``'degree_east'``, ``'degree_E'``,
        ``'degrees_E'``, ``'degreeE'``, and ``'degreesE'``.

        Note that units of ``'degrees'`` are not longitude units.

        .. seealso:: `isdimensionless`, `islatitude`, `ispressure`,
                     `isreftime`, `istime`

        **Examples:**

        >>> Units('degrees_east').islongitude
        True
        >>> Units('degrees').islongitude
        False
        >>> Units('degrees_north').islongitude
        False
        >>> Units('kg').islongitude
        False
        >>> Units().islongitude
        False

        """
        return self._units in (
            "degrees_east",
            "degree_east",
            "degree_E",
            "degrees_E",
            "degreeE",
            "degreesE",
        )

    @property
    def istime(self):
        """True if the units are time units, false otherwise.

        Note that reference time units (such as ``'days since
        2000-12-1'``) are not time units, nor are calendar years and
        calendar months.

        .. seealso:: `iscalendartime`, `isdimensionless`, `islongitude`,
                     `islatitude`, `ispressure`, `isreftime`

        **Examples:**

        >>> Units('days').istime
        True
        >>> Units('seconds').istime
        True
        >>> Units('kg').istime
        False
        >>> Units().istime
        False
        >>> Units('hours since 2100-1-1', calendar='noleap').istime
        False
        >>> Units(calendar='360_day').istime
        False
        >>> Units('calendar_years').istime
        False
        >>> Units('calendar_months').istime
        False

        """
        if self._isreftime:
            return False

        ut_unit = self._ut_unit
        if ut_unit is None:
            return False

        return bool(_ut_are_convertible(ut_unit, _day_ut_unit))

    @property
    def isvalid(self):
        """Whether the units are valid.

        .. seealso:: `reason_notvalid`

        **Examples:**

        >>> u = Units('km')
        >>> u.isvalid
        True
        >>> u.reason_notvalid
        ''

        >>> u = Units('Bad Units')
        >>> u.isvalid
        False
        >>> u.reason_notvalid
        "Invalid units: 'Bad Units'; Not recognised by UDUNITS"
        >>> u = Units('days since 2000-1-1', calendar='Bad Calendar')
        >>> u.isvalid
        False
        >>> u.reason_notvalid
        "Invalid calendar='Bad Calendar'; calendar must be one of ['standard', 'gregorian', 'proleptic_gregorian', 'noleap', 'julian', 'all_leap', '365_day', '366_day', '360_day'], got 'bad calendar'"

        """
        return getattr(self, "_isvalid", False)

    @property
    def reason_notvalid(self):
        """The reason that units are considered invalid.

        If the units are valid then the reason is an empty string.

        .. seealso:: `isvalid`

        **Examples:**

        >>> u = Units('km')
        >>> u.isvalid
        True
        >>> u.reason_notvalid
        ''

        >>> u = Units('Bad Units')
        >>> u.isvalid
        False
        >>> u.reason_notvalid
        "Invalid units: 'Bad Units'; Not recognised by UDUNITS"

        >>> u = Units('days since 2000-1-1', calendar='Bad Calendar')
        >>> u.isvalid
        False
        >>> u.reason_notvalid
        "Invalid calendar='Bad Calendar'; calendar must be one of ['standard', 'gregorian', 'proleptic_gregorian', 'noleap', 'julian', 'all_leap', '365_day', '366_day', '360_day'], got 'bad calendar'"

        """
        return getattr(self, "_reason_notvalid", "")

    @property
    def reftime(self):
        """The reference date-time of reference time units.

        .. seealso:: `calendar`, `isreftime`, `units`

        :Returns:

            `cftime.datetime`

        **Examples:**

        >>> u = Units('days since 2001-01-01', calendar='360_day')
        >>> u.reftime
        cftime.datetime(2001, 1, 1, 0, 0, 0, 0, calendar='360_day', has_year_zero=False)

        """
        if self.isreftime:
            # utime = self._utime
            # if utime:
            #     origin = utime.origin
            #     if origin:
            #         if isinstance(origin, datetime.datetime):
            #             return cftime.datetime(*origin.timetuple()[:7])
            #         else:
            #             origin
            # else:
            #     # Some refrence date-times do not have a utime, such
            #     # as those defined by months or years

            #            calendar = self._canonical_calendar
            #            return cftime.datetime(
            #                *cftime._parse_date(self.units.split(" since ")[1])[:7],
            #                calendar=calendar

            #            )

            # Make some mock reference time units with day (or
            # anything other than months/years)
            units = f"day since {self.units.split(' since ')[1]}"

            return cftime_dateparse(units, calendar=self._canonical_calendar)

        raise AttributeError(f"{self!r} has no attribute 'reftime'")

    @property
    def calendar(self):
        """The calendar for reference time units.

        May be any string allowed by the calendar CF property.

        If it is unset then the default CF calendar is assumed when
        required.

        .. seealso:: `units`

        **Examples:**

        >>> Units(calendar='365_day').calendar
        '365_day'
        >>> Units('days since 2001-1-1', calendar='noleap').calendar
        'noleap'
        >>> Units('days since 2001-1-1').calendar
        Traceback (most recent call last):
            ...
        AttributeError: Units has no attribute 'calendar'

        """
        value = self._calendar
        if value is not None:
            return value

        raise AttributeError(
            f"{self.__class__.__name__} has no attribute 'calendar'"
        )

    @property
    def units(self):
        """The units.

        May be any string allowed by the units CF property.

        .. seealso:: `calendar`

        **Examples:**

        >>> Units('kg').units
        'kg'
        >>> Units('seconds').units
        'seconds'
        >>> Units('days since 2000-1-1', calendar='366_day').units
        'days since 2000-1-1'

        """
        value = self._units
        if value is not None:
            return value

        raise AttributeError(
            f"{self.__class__.__name__} object has no attribute 'units'"
        )

    # ----------------------------------------------------------------
    # Methods
    # ----------------------------------------------------------------
    def equivalent(self, other, verbose=False):
        """Tests whether two units are numerically convertible.

        Returns True if numeric values in one unit are convertible to
        numeric values in the other unit.

        .. seealso:: `equals`

        :Parameters:

            other: `Units`
                The other units.

        :Returns:

            `bool`
                True if the units are equivalent, False otherwise.

        **Examples:**

        >>> u = Units('m')
        >>> v = Units('km')
        >>> w = Units('s')

        >>> u.equivalent(v)
        True
        >>> u.equivalent(w)
        False

        >>> u = Units('days since 2000-1-1')
        >>> v = Units('days since 2000-1-1', calendar='366_day')
        >>> w = Units('seconds since 1978-3-12', calendar='gregorian')

        >>> u.equivalent(v)
        False
        >>> u.equivalent(w)
        True

        Invalid units are not equivalent:

        >>> Units('bad units').equivalent(Units('bad units'))
        False

        """
        #        if not self.isvalid or not other.isvalid:
        #            return False

        isreftime1 = self._isreftime
        isreftime2 = other._isreftime

        #        if isreftime1 and isreftime2:
        #            # Both units are reference-time units
        #            if self._canonical_calendar != other._canonical_calendar:
        #                if verbose:
        #                    print("{}: Incompatible calendars: {!r}, {!r}".format(
        #                        self.__class__.__name__,
        #                        self._calendar, other._calendar))  # pragma: no cover
        #                return False
        #
        #            reftime0 = getattr(self, 'reftime', None)
        #            reftime1 = getattr(other, 'reftime', None)
        #            if reftime0 != reftime1:
        #                if verbose:
        #                    print(
        #                        "{}: Different reference date-times: "
        #                        "{!r}, {!r}".format(
        #                            self.__class__.__name__,
        #                            reftime0, reftime1
        #                        )
        #                    )  # pragma: no cover
        #                return False
        #
        #        elif isreftime1 or isreftime2:
        #            if verbose:
        #                print("{}: Only one is reference time".format(
        #                    self.__class__.__name__))  # pragma: no cover
        #            return False

        if isreftime1 and isreftime2:
            # Both units are reference-time units
            units0 = self._units
            units1 = other._units
            if units0 and units1 or (not units0 and not units1):
                out = self._canonical_calendar == other._canonical_calendar
                if verbose and not out:
                    print(
                        f"{self.__class__.__name__}: Incompatible calendars: "
                        f"{self._calendar!r}, {other._calendar!r}"
                    )  # pragma: no cover

                return out
            else:
                return False

        elif isreftime1 or isreftime2:
            if verbose:
                print(
                    f"{self.__class__.__name__}: Only one is reference time"
                )  # pragma: no cover
            return False

        #        if not self.isvalid:
        #            if verbose:
        #                print(
        #                    "{}: {!r} is not valid".format(
        #                        self.__class__.__name__, self)
        #                )  # pragma: no cover
        #            return False
        #
        #        if not other.isvalid:
        #            if verbose:
        #                print(
        #                    "{}: {!r} is not valid".format(
        #                        self.__class__.__name__, other)
        #                )  # pragma: no cover
        #            return False

        #         if isreftime1 and isreftime2:
        #            # Both units are reference-time units
        #            units0 = self._units
        #            units1 = other._units
        #            if units0 and units1 or (not units0 and not units1):
        #                return self._calendar == other._calendar
        #            else:
        #                return False

        # Still here?
        if self._units is None and other._units is None:
            # Both units are null and therefore equivalent (updated
            # test criteria at v3.3.1)
            return True

        # Units('') and Units() are equivalent. v3.3.0 (updated test
        # criteria at v3.3.1)
        if self._units in (None, "") and other._units in (None, ""):
            return True

        return bool(_ut_are_convertible(self._ut_unit, other._ut_unit))

    def formatted(self, names=None, definition=None):
        """Formats the `units` attribute string in a standardised way.

        The `units` attribute is modified in place and its new value
        is returned.

        :Parameters:

            names: `bool`, optional
                Use unit names instead of symbols.

            definition: `bool`, optional
                The formatted string is given in terms of basic units
                instead of stopping any expansion at the highest level
                possible.

        :Returns:

            `str` or `None`
                The formatted string. If the units have not yet been set,
                then `None` is returned.

        **Examples:**

        >>> u = Units('W')
        >>> u.units
        'W'
        >>> u.formatted(names=True)
        'watt'
        >>> u.formatted(definition=True)
        'm2.kg.s-3'
        >>> u.formatted(names=True, definition=True)
        'meter^2-kilogram-second^-3'
        >>> u.formatted()
        'W'

        >>> u = Units('dram')
        >>> u.formatted(names=True)
        '0.001771845 kilogram'

        >>> u = Units('hours since 2100-1-1', calendar='noleap')
        >>> u.formatted(names=True)
        'hour since 2100-01-01 00:00:00'
        >>> u.formatted()
        'h since 2100-01-01 00:00:00'

        Formatting is also available during object initialization:

        >>> u = Units('m/s', formatted=True)
        >>> u.units
        'm.s-1'

        >>> u = Units('dram', names=True)
        >>> u.units
        '0.001771845 kilogram'

        >>> u = Units('Watt')
        >>> u.units
        'Watt'

        >>> u = Units('Watt', formatted=True)
        >>> u.units
        'W'

        >>> u = Units('Watt', names=True)
        >>> u.units
        'watt'

        >>> u = Units('Watt', definition=True)
        >>> u.units
        'm2.kg.s-3'

        >>> u = Units('Watt', names=True, definition=True)
        >>> u.units
        'meter^2-kilogram-second^-3'

        """
        ut_unit = self._ut_unit

        if ut_unit is None:
            return None

        opts = _UT_ASCII
        if names:
            opts |= _UT_NAMES
        if definition:
            opts |= _UT_DEFINITION

        if _ut_format(ut_unit, _string_buffer, _sizeof_buffer, opts) != -1:
            out = _string_buffer.value
        else:
            raise ValueError(f"Can't format unit {self!r}")

        if self.isreftime:
            out = str(out, "utf-8")  # needs converting from byte-string
            out += " since " + self.reftime.strftime()
            return out

        return out.decode("utf-8")

    @classmethod
    def conform(cls, x, from_units, to_units, inplace=False):
        """Conforms values to equivalent values in a compatible unit.

        Returns the conformed values.

        The values may either be a `numpy` array, a Python numeric type,
        or a `list` or `tuple`. The returned value is of the same type,
        except that input integers are converted to floats and Python
        sequences are converted to `numpy` arrays (see the *inplace*
        keyword).

        .. warning:: Do not change the calendar of reference time units in
                     the current version. Whilst this is possible, it will
                     almost certainly result in an incorrect
                     interpretation of the data or an error.

        :Parameters:

            x: `numpy.ndarray` or Python numeric type or `list` or `tuple`

            from_units: `Units`
                The original units of *x*

            to_units: `Units`
                The units to which *x* should be conformed to.

            inplace: `bool`, optional
                If True and *x* is a `numpy` array then change it in place,
                creating no temporary copies, with one exception: If *x*
                is of integer type and the conversion is not null, then it
                will not be changed inplace and the returned conformed
                array will be of float type.

                If *x* is a `list` or `tuple` then the *inplace* parameter
                is ignored and a `numpy` array is returned.

        :Returns:

            `numpy.ndarray` or Python numeric
                The modified numeric values.

        **Examples:**

        >>> Units.conform(2, Units('km'), Units('m'))
        2000.0

        >>> import numpy
        >>> a = numpy.arange(5.0)
        >>> Units.conform(a, Units('minute'), Units('second'))
        array([   0.,   60.,  120.,  180.,  240.])
        >>> print(a)
        [0. 1. 2. 3. 4.]

        >>> Units.conform(
        ...     a,
        ...     Units('days since 2000-12-1'),
        ...     Units('days since 2001-1-1'),
        ...     inplace=True
        ... )
        array([-31., -30., -29., -28., -27.])
        >>> print(a)
        [-31. -30. -29. -28. -27.]

        """
        value_error = ValueError(
            f"Units are not convertible: {from_units!r}, {to_units!r}"
        )

        if from_units.equals(to_units):
            if not isinstance(x, (int, float)):
                x = numpy_asanyarray(x)

            if inplace:
                return x
            else:
                try:
                    return x.copy()
                except AttributeError:
                    x

        if not from_units.equivalent(to_units):
            raise value_error

        ut_unit1 = from_units._ut_unit
        ut_unit2 = to_units._ut_unit

        if ut_unit1 is None or ut_unit2 is None:
            raise value_error

        convert = _ut_compare(ut_unit1, ut_unit2)

        if from_units._isreftime and to_units._isreftime:
            # --------------------------------------------------------
            # Both units are time-reference units, so calculate the
            # non-zero offset in units of days.
            # --------------------------------------------------------
            units0, reftime0 = from_units.units.split(" since ")
            units1, reftime1 = to_units.units.split(" since ")
            if units0 in _months_or_years:
                from_units = cls(
                    "days since " + reftime0,
                    calendar=getattr(from_units, "calendar", None),
                )
                x = numpy_asanyarray(x)
                if inplace:
                    if units0 in ("month", "months"):
                        x *= _month_length
                    else:
                        x *= _year_length
                else:
                    if units0 in ("month", "months"):
                        x = x * _month_length
                    else:
                        x = x * _year_length

                    inplace = True

                ut_unit1 = from_units._ut_unit
                ut_unit2 = to_units._ut_unit

                convert = _ut_compare(ut_unit1, ut_unit2)

            if units1 in _months_or_years:
                to_units = cls(
                    "days since " + reftime1,
                    calendar=getattr(to_units, "calendar", None),
                )

            #            to_jd0 = cftime.JulianDayFromDate(
            #                to_units._utime.origin, calendar=to_units._utime.calendar
            #            )
            to_jd0 = to_units._utime.toordinal(fractional=True)
            #            from_jd0 = cftime.JulianDayFromDate(
            #                from_units._utime.origin, calendar=from_units._utime.calendar
            #           )
            from_jd0 = from_units._utime.toordinal(fractional=True)

            offset = to_jd0 - from_jd0
        else:
            offset = 0

        # ------------------------------------------------------------
        # If the two units are identical then no need to alter the
        # value, so return it unchanged.
        # ------------------------------------------------------------
        #        if not convert and not offset:
        #            return x

        if convert:
            cv_converter = _ut_get_converter(ut_unit1, ut_unit2)
            if not cv_converter:
                _cv_free(cv_converter)
                raise value_error

        # ------------------------------------------------------------
        # Find out if x is (or should be) a numpy array or a Python
        # number
        # ------------------------------------------------------------
        if isinstance(x, numpy_generic):
            # Convert a generic numpy scalar to a 0-d numpy array
            x = numpy_array(x)
            x_is_numpy = True
        elif not isinstance(x, numpy_ndarray):
            if numpy_size(x) > 1 or len(numpy_shape(x)):
                # Convert a non-numpy (possibly nested) sequence to a
                # numpy array. E.g. [1], ((1.5, 2.5))
                x = numpy_asanyarray(x)
                x_is_numpy = True
                inplace = True
            else:
                x_is_numpy = False
        else:
            x_is_numpy = True

        if x_is_numpy:
            if not x.flags.contiguous:
                x = numpy_array(x, order="C")
            # TODO DCH

            # --------------------------------------------------------
            # Convert an integer numpy array to a float numpy array
            # --------------------------------------------------------
            if inplace:
                if x.dtype.kind == "i":
                    # Here it is only checked for signed integer:
                    # Are unsigned integers not possible?
                    if x.dtype.itemsize in (1, 2):
                        # Inplace converting is not possible in this case:
                        # If x uses only 1 byte for each element, there is
                        # no adequate float available from numpy
                        # (smallest float uses 2 bytes: float16).
                        # ctypes does not provide something like a float16.
                        x = x.astype("float32")
                    else:
                        new_dtype = x.dtype.str.replace("i", "f")
                        y = x.view(dtype=new_dtype)
                        y[...] = x
                        x.dtype = numpy_dtype(new_dtype)
            else:
                # At numpy vn1.7 astype has many more keywords ...
                if x.dtype.kind == "i":
                    if x.dtype.char == "i":
                        x = x.astype("float32")
                    elif x.dtype.char == "l":
                        x = x.astype(float)
                else:
                    x = x.copy()

        # ------------------------------------------------------------
        # Convert the array to the new units
        # ------------------------------------------------------------
        if convert:

            if x_is_numpy:
                # Create a pointer to the array cast to the
                # appropriate ctypes object
                itemsize = x.dtype.itemsize
                pointer = x.ctypes.data_as(_ctypes_POINTER[itemsize])

                # Convert the array in place
                _cv_convert_array[itemsize](
                    cv_converter, pointer, _c_size_t(x.size), pointer
                )
            else:
                # Create a pointer to the number cast to a ctypes
                # double object.
                y = _c_double(x)
                pointer = ctypes.pointer(y)
                # Convert the pointer
                _cv_convert_doubles(
                    cv_converter, pointer, _c_size_t(1), pointer
                )
                # Reset the number
                x = y.value

            _cv_free(cv_converter)

        # ------------------------------------------------------------
        # Apply an offset for reference-time units
        # ------------------------------------------------------------
        if offset:
            # Convert the offset from 'days' to the correct units and
            # subtract it from x
            if _ut_compare(_day_ut_unit, ut_unit2):

                cv_converter = _ut_get_converter(_day_ut_unit, ut_unit2)
                scale = numpy_array(1.0)
                pointer = scale.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
                _cv_convert_doubles(
                    cv_converter, pointer, _c_size_t(scale.size), pointer
                )
                _cv_free(cv_converter)

                offset *= scale.item()

            x -= offset

        return x

    def copy(self):
        """Returns a deep copy.

        Equivalent to ``copy.deepcopy(u)``.

        :Returns:

                The deep copy.

        **Examples:**

        >>> u = Units('decibel')
        >>> v = u.copy()
        >>> v
        <Units: decibel>

        """
        return self

    def equals(self, other, rtol=None, atol=None, verbose=False):
        """Tests if units are numerically convertible to equal value.

        Returns True if and only if numeric values in one unit are
        convertible to numeric values in the other unit and their
        conversion is a scale factor of 1.

        .. seealso:: `equivalent`

        :Parameters:

            other: `Units`
                The other units.

        :Returns:

            `bool`
                `True` if the units are equal, `False` otherwise.

        **Examples:**

        >>> u = Units('km')
        >>> v = Units('1000m')
        >>> w = Units('100000m')
        >>> u.equals(v)
        True
        >>> u.equals(w)
        False

        >>> u = Units('m s-1')
        >>> m = Units('m')
        >>> s = Units('s')
        >>> u.equals(m)
        False
        >>> u.equals(m/s)
        True
        >>> (m/s).equals(u)
        True

        Undefined units are considered equal:

        >>> u = Units()
        >>> v = Units()
        >>> u.equals(v)
        True

        Invalid units are not equal:

        >>> Units('bad units').equals(Units('bad units'))
        False

        """
        isreftime1 = self._isreftime
        isreftime2 = other._isreftime

        if isreftime1 and isreftime2:
            # Both units are reference-time units
            if self._canonical_calendar != other._canonical_calendar:
                if verbose:
                    print(
                        f"{self.__class__.__name__}: Incompatible calendars: "
                        f"{self._calendar!r}, {other._calendar!r}"
                    )  # pragma: no cover

                return False

            reftime0 = getattr(self, "reftime", None)
            reftime1 = getattr(other, "reftime", None)
            if reftime0 != reftime1:
                if verbose:
                    print(
                        f"{self.__class__.__name__}: Different reference "
                        f"date-times: {reftime0!r}, {reftime1!r}"
                    )  # pragma: no cover

                return False

        elif isreftime1 or isreftime2:
            if verbose:
                print(
                    f"{self.__class__.__name__}: Only one is reference time"
                )  # pragma: no cover

            return False

        #            utime0 = self._utime
        #            utime1 = other._utime
        #            if utime0 is not None and utime1 is not None:
        #                return utime0.origin_equals(utime1)
        #            elif utime0 is None and utime1 is None:
        #                return self.reftime
        #
        #
        #
        #            units0 = self._units
        #            units1 = other._units
        #            if units0 and units1 or (not units0 and not units1):
        #                out = (self._canonical_calendar == other._canonical_calendar)
        #                if verbose and not out:
        #                    print("{}: Incompatible calendars: {!r}, {!r}".format(
        #                        self.__class__.__name__,
        #                        self._calendar, other._calendar))  # pragma: no cover
        #
        #                return out
        #            else:
        #                return False

        #        if not self.isvalid:
        #            if verbose:
        #                print(
        #                    "{}: {!r} is not valid".format(
        #                        self.__class__.__name__, self)
        #                )  # pragma: no cover
        #            return False
        #
        #        if not other.isvalid:
        #            if verbose:
        #                print(
        #                    "{}: {!r} is not valid".format(
        #                        self.__class__.__name__, other)
        #                )  # pragma: no cover
        #            return False
        #

        #        if not self.isvalid or not other.isvalid:
        #            print ('ppp')
        #            return False

        if self._units is None and other._units is None:
            # Both units are null and therefore equal (v3.3.1)
            return True

        if self._ut_unit is None and other._ut_unit is None:
            # Both units are invalid (v3.3.1)
            return False

        try:
            if not _ut_compare(self._ut_unit, other._ut_unit):
                return True

            if verbose:
                print(
                    f"{self.__class__.__name__}: Different units: "
                    f"{self.units!r}, {other.units!r}"
                )  # pragma: no cover

            return False
        except AttributeError:
            return False

    def log(self, base):
        """Returns the logarithmic unit corresponding to a log base.

        :Parameters:

            base: `int` or `float`
                The logarithmic base.

        :Returns:

            `Units`
                The logarithmic unit corresponding to the given
                logarithmic base.

        **Examples:**

        >>> u = Units('W', names=True)
        >>> u
        <Units: watt>

        >>> u.log(10)
        <Units: lg(re 1 W)>
        >>> u.log(2)
        <Units: lb(re 1 W)>

        >>> import math
        >>> u.log(math.e)
        <Units: ln(re 1 W)>

        >>> u.log(3.5)
        <Units: 0.798235600147928 ln(re 1 W)>

        """
        try:
            _ut_unit = _ut_log(_c_double(base), self._ut_unit)
        except TypeError:
            pass
        else:
            if _ut_unit:
                return type(self)(_ut_unit=_ut_unit)

        raise ValueError(
            f"Can't take the logarithm to the base {base!r} of {self!r}"
        )


# class Utime:  # cftime.utime):
#    """Converts netCDF time coordinate data to/from datetime objects.
#
#    This object is (currently) functionally equivalent to a
#    `netCDF4.netcdftime.utime` object.
#
#    **Attributes**
#
#    ==============  ==================================================
#    Attribute       Description
#    ==============  ==================================================
#    `!calendar`     The calendar used in the time calculation.
#    `!origin`       A date/time object for the reference time.
#    `!tzoffset`     Time zone offset in minutes.
#    `!unit_string`
#    `!units`
#    ==============  ==================================================
#
#    """
#
#    def __init__(
#        self, calendar, unit_string=None, only_use_cftime_datetimes=True
#    ):
#        """Initialises the `Utime` instance.
#
#        :Parameters:
#
#            calendar: `str`
#                The calendar used in the time calculations. Must be one
#                of: ``'gregorian'``, ``'360_day'``, ``'365_day'``,
#                ``'366_day'``, ``'julian'``, ``'proleptic_gregorian'``,
#                although this is not checked.
#
#            unit_string: `str`, optional
#                A string of the form "time-units since <time-origin>"
#                defining the reference-time units.
#
#            only_use_cftime_datetimes: `bool`, optional
#                If False, datetime.datetime objects are returned from
#                `num2date` where possible; By default. dates which
#                subclass `cftime.datetime` are returned for all calendars.
#
#        """
#        if unit_string:
#            super().__init__(
#                unit_string,
#                calendar,
#                only_use_cftime_datetimes=only_use_cftime_datetimes,
#            )
#        else:
#            self.calendar = calendar
#            self.origin = None
#            self.tzoffset = None
#            self.unit_string = None
#            self.units = None
#
#    def __repr__(self):
#        """Returns a printable representation of the `Utime` object.
#
#        x.__repr__() is logically equivalent to repr(x).
#
#        """
#        unit_string = self.unit_string
#        if unit_string:
#            x = [unit_string]
#        else:
#            x = []
#
#        x.append(self.calendar)
#
#        return "<Utime: {}>".format(" ".join(x))
#
#    def num2date(self, time_value):
#        """Returns a datetime-like object given a time value.
#
#        The units of the time value are described by the `!unit_string`
#        and `!calendar` attributes.
#
#        See `netCDF4.netcdftime.utime.num2date` for details.
#
#        In addition to `netCDF4.netcdftime.utime.num2date`, this method
#        handles units of months and years as defined by Udunits, ie. 1
#        year = 365.242198781 days, 1 month = 365.242198781/12 days.
#
#        """
#        units = self.units
#        unit_string = self.unit_string
#
#        if units in ("month", "months"):
#            # Convert months to days
#            unit_string = unit_string.replace(units, "days", 1)
#            time_value = numpy_array(time_value) * _month_length
#        elif units in ("year", "years", "yr"):
#            # Convert years to days
#            unit_string = unit_string.replace(units, "days", 1)
#            time_value = numpy_array(time_value) * _year_length
#
#        u = cftime.utime(unit_string, self.calendar)
#
#        return u.num2date(time_value)
