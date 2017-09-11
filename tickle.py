#!/usr/bin/env python3

import sys
from logging import warning
import argparse
import fileinput
import re
from datetime import date, timedelta

class Tickler:
  """ tickler reminder system """

  def __init__(self):
    self.tickle_regex = re.compile(r"""
        ^
        (?P<indent> \s*)      # capture indentation
        [#]\s*tickle\s+       # recognize the "# tickle" prefix
        (                     #
          (?P<date_spec> .*?) # capture date_spec
          \s+                 #
        )?                    #
        say(?:ing)?\s*        # recognize "say(ing)"
        (?P<message> .*)      # capture tickler message
        $
      """
      , re.IGNORECASE | re.VERBOSE
    )

    self.date_tests = [ ]
    self.date_tests.append(self.test_date_spec_none)
    self.date_tests.append(self.test_date_spec_daily)
    self.date_tests.append(self.test_date_spec_on_date)
    self.date_tests.append(self.test_date_spec_weekly)
    self.date_tests.append(self.test_date_spec_monthly)
    self.date_tests.append(self.test_date_spec_yearly)

  def __call__(self, argv):
    self.process_tickler_files(argv)

  def process_tickler_files(self, argv):
    """ process tickler commands from files specified on the command line """

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--echo', action='store_true')
    parser.add_argument('-m', '--merge', action='store_true')
    parser.add_argument('-d', '--date')
    parser.add_argument('ticklers', nargs='*')
    args = parser.parse_args()

    td = TicklerDate(args.date)

    with fileinput.input(files = args.ticklers, inplace = args.merge) as files:
      for line in files:
        sys.stdout.write(self.process_tickle(line, td))
        if args.echo or args.merge:
          # echo all lines without modification
          sys.stdout.write(line)

  def process_tickle(self, line, tickle_date = None):
    """ determines if line is a tickle and if so, determine if the tickle matches
        the date, and if so, returns a formated message - otherwise,
        returns ''
    """

    m = self.tickle_regex.match(line)
    if m:
      if self.test_tickle_date(m.group('date_spec'), tickle_date):
        return self.format_tickle(m.group('message'), m.group('indent'))
      else:
        return ''

    else:
      return ''

  def test_tickle_date(self, date_spec, tickle_date):
    """ return True if the date matches the date_spec, otherwise return False """

    ds = date_spec.lower().strip() if date_spec else None
    assert isinstance(tickle_date, TicklerDate) \
      , "tickle_date argument must be a TicklerDate object"

    for date_test in self.date_tests:
      # match == True means date_spec matchs a recognized format
      # test  == True means date_spec matchs the date
      match, test = date_test(ds, tickle_date)
      if match: return test

    warning("unmatched date_spec '%s'" % ds)
    return False

  def test_date_spec_none(self, date_spec, tickle_date):
    if date_spec is None: return True, True
    else: return False, False

  def test_date_spec_daily(self, date_spec, tickle_date):
    if re.match(r'daily', date_spec, re.IGNORECASE): return True, True
    else: return False, False

  def test_date_spec_on_date(self, date_spec, tickle_date):
    m = re.match(r'on\s+(.*)', date_spec, re.IGNORECASE)
    if m: return True, TicklerDate(m.group(1)) == tickle_date
    else: return False, False

  def test_date_spec_weekly(self, date_spec, tickle_date):
    m = re.match(r'^weekly\s+(.*)$', date_spec, re.IGNORECASE)
    if m:
      for weekday in re.split(r'\W+', m.group(1)):
        if tickle_date.is_weekday(weekday):
          return True, True
      return True, False
    else: return False, False

  def test_date_spec_monthly(self, date_spec, tickle_date):
    m = re.match(r'^monthly\s+(.*)$', date_spec, re.IGNORECASE)
    if m:
      for day_of_month in re.split(r'\s*,\s*', m.group(1)):
        if tickle_date.is_monthday(day_of_month):
          return True, True
      return True, False
    else: return False, False

  def test_date_spec_yearly(self, date_spec, tickle_date):
    m = re.match(r'^yearly\s+(.*)$', date_spec, re.IGNORECASE)
    if m:
      for day_of_year in re.split(r'\s*,\s*', m.group(1)):
        if tickle_date.is_yearday(day_of_year):
          return True, True
      return True, False
    else: return False, False

  def format_tickle(self, message, indentation):
    """ return a formatted tickle message, preserving original indentation """

    return indentation + message.strip() + "\n"

################################################################################

def get_iso_date(year, month, day):
  """ wrapper to handle exceptions when creating a datetime.date object """

  y, m, d = int(year), int(month), int(day)

  try:
    d = date(y, m, d)
  except ValueError as e:
    warning("invalid date: %s" % e)
    return None
  else:
    return d

def read_iso_date(day):
  """ is date in an ISO-8601-like date format """

  m = re.match(r'^(\d{1,4})-(\d{1,2})-(\d{1,2})$', day)
  if m:
    d = get_iso_date(m.group(1), m.group(2), m.group(3))

    if d: return True, d
    else: return False, None
  else: return False, None

def read_today(day):
  """ is date 'today' """

  if 'today' == day.lower():
    return True, date.today()
  else: return False, None

def read_tomorrow(day):
  """ is date 'tomorrow' """

  if 'tomorrow' == day.lower():
    return True, date.today() + timedelta(days = 1)
  else: return False, None

def read_overmorrow(day):
  """ is date 'overmorrow' """

  if 'overmorrow' == day.lower():
    return True, date.today() + timedelta(days = 2)
  else: return False, None

def read_yesterday(day):
  """ is date 'yesterday' """

  if 'yesterday' == day.lower():
    return True, date.today() + timedelta(days = -1)
  else: return False, None

def read_ereyesterday(day):
  """ is date 'ereyesterday' """

  if 'ereyesterday' == day.lower():
    return True, date.today() + timedelta(days = -2)
  else: return False, None

def read_date(day = None):
  """ reads a date in multiple formats, returns a datetime.date object """

  date_format_tests = []
  date_format_tests.append(read_iso_date)
  date_format_tests.append(read_today)
  date_format_tests.append(read_tomorrow)
  date_format_tests.append(read_overmorrow)
  date_format_tests.append(read_yesterday)
  date_format_tests.append(read_ereyesterday)

  if not day:
    return date.today()
  else:
    d = str(day).strip()

    for test in date_format_tests:
      success, date_string = test(d)
      if success: return date_string

    warning("unrecognized date '%s'" % d)
    return date.today()

def ordinal_to_int(ordinal):
  ordinals = {
    'zeroth':      0
    , 'first':     1
    , 'second':    2
    , 'third':     3
    , 'fourth':    4
    , 'fifth':     5
    , 'sixth':     6
    , 'seventh':   7
    , 'eighth':    8
    , 'ninth':     9
    , 'tenth':    10
    , 'eleventh': 11
    , 'twelfth':  12
  }
  numeric_ordinal = re.match(r"^([0-9]+)", ordinal)
  if numeric_ordinal:
    return int(numeric_ordinal.group(1))
  elif ordinal in ordinals:
    return ordinals[ordinal]
  else:
    return None

class TicklerDate:
  def __init__(self, day = None):
    self.date = read_date(day)
    assert self.date, "TicklerDate.date failed to initialize"

    self.weekday_names = {
      'monday':      0
      , 'mon':       0
      , 'm':         0
      , 'tuesday':   1
      , 'tue':       1
      , 'tues':      1
      , 't':         1
      , 'wednesday': 2
      , 'wed':       2
      , 'wednes':    2
      , 'w':         2
      , 'thursday':  3
      , 'thu':       3
      , 'thur':      3
      , 'thurs':     3
      , 'th':        3
      , 'r':         3
      , 'friday':    4
      , 'fri':       4
      , 'f':         4
      , 'saturday':  5
      , 'sat':       5
      , 's':         5
      , 'sunday':    6
      , 'sun':       6
      , 'u':         6
    }

    self.month_names = {
      'january':     1
      , 'jan':       1
      , 'february':  2
      , 'feb':       2
      , 'march':     3
      , 'mar':       3
      , 'april':     4
      , 'apr':       4
      , 'may':       5
      , 'june':      6
      , 'jun':       6
      , 'july':      7
      , 'jul':       7
      , 'august':    8
      , 'aug':       8
      , 'september': 9
      , 'sept':      9
      , 'sep':       9
      , 'october':  10
      , 'oct':      10
      , 'november': 11
      , 'nov':      11
      , 'december': 12
      , 'dec':      12
    }

  def __str__(self): return str(self.date)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.date == other.date
    else:
      return False

  def is_weekday(self, weekday):
    """ return True if self.date is the day of the week in weekday """

    if weekday in self.weekday_names:
      return self.date.weekday() == self.weekday_names[weekday]
    else:
      warning("unrecognized weekday name '%s'" % weekday)
      return False

  def is_monthday(self, monthday):
    """ return True if self.date is the day of the month specified in monthday

        examples:
          10, 25  # on the tenth and twenty-fifth day of the month
          1st wed # on the first Wednesday of the month
          last day # on the last day of the month
          2 days before last day # two days before the last day of the month
    """

    simple_monthday = re.match(r'^[0-9]+$', monthday)
    if simple_monthday:
      return self.date.day == int(monthday)

    ordinal_monthday = re.match(
      r"""
        ^
        (?:
          (?P<ord> [1-5]|1st|first|2nd|second|3rd|third|4th|fourth|5th|fifth)
          \s+
        )?
        (?:
          (?P<last> last)
          \s+
        )?
        (?P<weekday> %s)
        $
      """ % '|'.join(self.weekday_names.keys())
      , monthday
      , re.IGNORECASE | re.VERBOSE
    )
    if ordinal_monthday:
      ordinal = 1
      if ordinal_monthday.group('ord'):
        ordinal = ordinal_to_int(ordinal_monthday.group('ord'))

      if not self.is_weekday(ordinal_monthday.group('weekday')):
        return False

      if ordinal_monthday.group('last'):
        mx = self.max_monthday()
        return mx - (7 * ordinal) < self.date.day <= mx - (7 * (ordinal - 1))
      else:
        return 7 * (ordinal - 1) < self.date.day <= (7 * ordinal)

    before_last_day = re.match(
      r"""
        ^
        (?:
          (?P<days_before> [0-9]+)
          \s*d(?:ay(?:s)?)?
          \s+before
          \s+
        )?
        last\s+day
        $
      """
      , monthday
      , re.IGNORECASE | re.VERBOSE
    )
    if before_last_day:
      days_before = 0
      if before_last_day.group('days_before'):
        days_before = int(before_last_day.group('days_before'))

      return self.date.day == self.max_monthday() - days_before

    warning("unrecognized day of month '%s'" % monthday)
    return False

  def max_monthday(self):
    """ return the maximum day of the month """
    m = self.date.month + 1
    y = self.date.year
    if m == 13:
      m = 1
      y += 1
    last_day_of_month = date(y, m, 1) + timedelta(days = -1)
    return last_day_of_month.day

  def is_leap_year(self):
    """ return True if self.date is in a leap year """

    if self.date.year % 4 == 0 and self.date.year %100 != 0:
      return True
    elif self.date.year % 400 == 0:
      return True
    else:
      return False

  def is_yearday(self, yearday):
    """ return True if self.date is the day of the year specified in yearday

        examples:
          100, 250 # on the 100th and 250th days of the year
    """

    simple_yearday = re.match(r'^[0-9]+$', yearday)
    if simple_yearday:
      yd = (self.date - date(self.date.year, 1, 1)).days + 1

      return yd == int(yearday)

    month_day = re.match(
      r"""
        ^
        (?P<month_name> %s)
        \s+
        (?P<day_of_month> [0-9]+)
        (?:st|nd|rd|th)?
        $
      """ % '|'.join(self.month_names.keys())
      , yearday
      , re.IGNORECASE | re.VERBOSE
    )
    day_month = re.match(
      r"""
        ^
        (?P<day_of_month> [0-9]+)
        (?:st|nd|rd|th)?
        \s+
        (?P<month_name> %s)
        $
      """ % '|'.join(self.month_names.keys())
      , yearday
      , re.IGNORECASE | re.VERBOSE
    )
    if month_day or day_month:
      mo = month_day if month_day else day_month
      y = self.date.year
      m = self.month_names[mo.group('month_name').lower()]
      d = int(mo.group('day_of_month'))

      if m == 2 and d == 29 and not self.is_leap_year():
        return False
      else:
        return self.date == date(y, m, d)

    return False

################################################################################

if __name__ == '__main__':
  Tickler()(sys.argv[1:])

# vim: set sw=2 ts=2:
