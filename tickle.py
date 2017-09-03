#!/usr/bin/env python3

import sys
from logging import warning
import argparse
import fileinput
import re
from datetime import date

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

  def __call__(self, argv):
    self.process_tickler_files(argv)

  def process_tickler_files(self, argv):
    """ process tickler commands from files specified on the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--echo', action='store_true')
    parser.add_argument('-m', '--merge', action='store_true')
    parser.add_argument('ticklers', nargs='*')
    args = parser.parse_args()

    with fileinput.input(files = args.ticklers, inplace = args.merge) as files:
      for line in files:
        sys.stdout.write(self.process_tickle(line))
        if args.echo or args.merge:
          # echo all lines without modification
          sys.stdout.write(line)

  def process_tickle(self, line):
    """ determines if line is a tickle and if so, determine if the tickle matches
        the date, and if so, returns a formated message - otherwise,
        returns ''
    """

    m = self.tickle_regex.match(line)
    if m:
      if self.test_tickle_date(m.group('date_spec')):
        return self.format_tickle(m.group('message'), m.group('indent'))
      else:
        return ''

    else:
      return ''

  def test_tickle_date(self, date_spec):
    """ return True if the date matches the date_spec, otherwise return False """
    if date_spec: date_spec = date_spec.lower().strip()

    for date_test in self.date_tests:
      # match = True means date_spec matchs a recognized format
      # test  = True means date_spec matchs the date
      match, test = date_test(date_spec)
      if match: return test

    warning("unmatched date_spec '%s'" % date_spec)
    return False

  def test_date_spec_none(self, date_spec):
    if date_spec is None: return True, True
    else: return False, False

  def test_date_spec_daily(self, date_spec):
    if re.match('daily', date_spec, re.IGNORECASE): return True, True
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

def read_date(day = None):
  """ reads a date in multiple formats, returns a datetime.date object """
  date_format_tests = []
  date_format_tests.append(read_iso_date)

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

################################################################################

if __name__ == '__main__':
  Tickler()(sys.argv[1:])
  #print(read_iso_date('199-2-15')[1])
  #print(get_iso_date('1000', '02', '01'))

  #td = TicklerDate('199-2-15')
  #print(td)

# vim: set sw=2 ts=2:
