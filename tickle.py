#!/usr/bin/env python3

import sys
from logging import warning
import argparse
import fileinput
import re

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

    self.add_date_test(
      lambda date_spec: date_spec is None
      , lambda date_spec: True # match every day
    )

    self.add_date_test(
      lambda date_spec: re.match('daily', date_spec, re.IGNORECASE)
      , lambda date_spec: True # match every day
    )

  def __call__(self, argv):
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

  def add_date_test(self, match, test):
    """ append a date test to the ordered list
          match(date_spec):
            returns True if the test function is appropriate for date_spec
          test(date_spec):
            returns True if date matches the date_spec
    """
    self.date_tests.append((match, test))

  def test_tickle_date(self, date_spec):
    """ return True if the date matches the date_spec, otherwise return False """
    # date_test is a list of tuples:  [0] is the test for whether the test in [1]
    # should be applied to the date_spec parameter

    if date_spec: date_spec = date_spec.lower().strip()

    for match, test in self.date_tests:
      if match(date_spec): return test(date_spec)

    warning("unmatched date_spec '%s'" % date_spec)
    return False

  def format_tickle(self, message, indentation):
    """ return a formatted tickle message, preserving original indentation """
    return indentation + message.strip() + "\n"

################################################################################

if __name__ == '__main__':
  Tickler()(sys.argv[1:])

# vim: set sw=2 ts=2:
