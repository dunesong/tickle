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
    return True, date.today() + timedelta(days=1)
  else: return False, None

def read_date(day = None):
  """ reads a date in multiple formats, returns a datetime.date object """
  date_format_tests = []
  date_format_tests.append(read_iso_date)
  date_format_tests.append(read_today)
  date_format_tests.append(read_tomorrow)

  if not day:
    return date.today()
  else:
    d = str(day).strip()

    for test in date_format_tests:
      success, date_string = test(d)
      if success: return date_string

    warning("unrecognized date '%s'" % d)
    return date.today()

class TicklerDate:
  def __init__(self, day = None):
    self.date = read_date(day)
    assert self.date, "TicklerDate.date failed to initialize"

  def __str__(self): return str(self.date)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.date == other.date
    else:
      return False

################################################################################

if __name__ == '__main__':
  Tickler()(sys.argv[1:])

# vim: set sw=2 ts=2:
