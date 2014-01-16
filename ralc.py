"""
====
ralc
====

Rate Calculator for multiplicate spent hours and rate per hour to find out how
many money you earned.

"""

from __future__ import print_function

import sys

from decimal import ROUND_UP, Decimal, DecimalException


__author__ = 'Igor Davydenko'
__license__ = 'BSD License'
__script__ = 'ralc'
__version__ = '0.1'


IS_PY3 = sys.version_info[0] == 3
ROUNDER = Decimal('.01')

integer_types = (int, ) if IS_PY3 else (int, long)  # noqa
text_types = (bytes, str) if IS_PY3 else (basestring, )  # noqa


class ValidationError(ValueError):
    """
    Validation error class.
    """


def calc(hours, rate):
    """
    Multiplicate spent hours with rate per hour to find out how many money has
    been earned.
    """
    return to_decimal(validate_hours(hours) * to_decimal(rate))


def main(*args):
    """
    Parse command line arguments and make calulcaiton if arguments is valid.
    """
    # Parse command line arguments
    args = parse_args(args or sys.argv[1:])

    # Make calculation and print result
    print('>', args.hours, 'x', args.rate, '=', calc(args.hours, args.rate))
    return False


def parse_args(args):
    """
    Parse command line arguments.
    """
    from argparse import ArgumentParser

    def rate_type(value):
        """
        Raise decimal exceptions as value errors.
        """
        try:
            return to_decimal(value)
        except DecimalException as err:
            raise ValueError(str(err))

    hours_type = validate_hours
    hours_type.__name__ = 'hours'
    rate_type.__name__ = 'rate'

    parser = ArgumentParser(description='Rate Calculator')
    parser.add_argument(
        'hours', help='Spent hours, e.g.: "30", "120:40", "10:55:30"',
        metavar='HH[:MM[:SS]]', type=hours_type
    )
    parser.add_argument(
        'rate', help='Rate per hour. Should be decimal value.',
        metavar='RATE', type=rate_type
    )

    return parser.parse_args(args)


def to_decimal(value):
    """
    Init decimal value and quantize it using default rounder.
    """
    if isinstance(value, float):
        value = str(round(value, 2))
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(ROUNDER, ROUND_UP)


def validate_hours(value):
    """
    Validate hours value and convert if it valid to Decimal.

    Valid schemas:

    * HH -> Hours:00:00, e.g.: 30
    * HH:MM -> Hours:Minutes:00, e.g.: 120:40
    * HH:MM:SS -> Hours:Minutes:Seconds, e.g.: 10:55:30

    """
    # If value is already decimal, or int, or float return it as quantized
    # decimal
    if isinstance(value, (Decimal, float) + integer_types):
        return to_decimal(value)

    # Now value should be a string, if not raise an error
    if not isinstance(value, text_types):
        raise ValidationError('Unsupported type for hours value: {0!r}'.
                              format(type(value.__class__.__name__)))

    counter = value.count(':')
    hours, minutes, seconds = 0, 0, 0

    if counter == 1:
        hours, minutes = value.split(':')
    elif counter == 2:
        hours, minutes, seconds = value.split(':')
    else:
        hours = value

    try:
        hours = to_decimal(hours)
        minutes = int(minutes)
        seconds = int(seconds)
    except (DecimalException, TypeError, ValueError):
        raise ValidationError('Invalid hours value. Please, use next format: '
                              'HH[:MM[:SS]]')

    return hours + to_decimal(Decimal(minutes * 60 + seconds) / Decimal(3600))


if __name__ == '__main__':
    sys.exit(int(main()))
