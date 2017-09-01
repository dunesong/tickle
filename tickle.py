#!/usr/bin/env python3

import sys
import os
import argparse
import re
from tempfile import mkstemp
from shutil import copystat

class Tickler:
  """ tickler reminder system """

  def __init__(self): pass

  def __call__(self, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--echo', action='store_true')
    parser.add_argument('-m', '--merge', action='store_true')
    parser.add_argument('tickler_file', nargs='+')
    args = parser.parse_args()

    for filename in args.tickler_file:
      if os.access(filename, os.R_OK):
        tickler = open(filename, 'r')
        if args.merge:
          tmp_fd, tmp_filepath = mkstemp(None, filename + '.', '.', True)
          tmp_file = open(tmp_filepath, 'w')

        for line in tickler:
          sys.stdout.write(self.process_tickle(line))
          if args.echo:
            # echo all lines without modification
            sys.stdout.write(line)
          if args.merge:
            tmp_file.write(line)

        tickler.close()
        if args.merge:
          tmp_file.flush()
          os.fsync(tmp_fd)
          os.close(tmp_fd)
          try:
            copystat(filename, tmp_filepath)
          except WindowsError:
            pass # can't copy file acces time
          os.replace(tmp_filepath, filename)


  def process_tickle(self, line):
    """ determines if line is a tickle and if so, determine if the tickle matches 
        the date, and if so, returns a formated message - otherwise, 
        returns '' 
    """

    tickle_regex = re.compile(r"""
        ^
        (?P<indent> \s*)
        [#]\s*tickle\s+
        (
          (?P<date_spec> .*?)
          \s+
        )?
        say(?:ing)?\s*
        (?P<message> .*)
        $
      """
      , re.IGNORECASE | re.VERBOSE
    )

    m = tickle_regex.match(line)
    if m:
      indent = m.group('indent')
      date_spec = m.group('date_spec')
      if date_spec: 
        date_spec = date_spec.lower().strip()
      else:
        # if no date specification, default to daily
        date_spec = 'daily'
      message = m.group('message')

      if self.test_tickle_date(date_spec):
        return self.format_tickle(m.group('message'), m.group('indent'))
      else:
        return ''

    else:
      return ''

  def test_tickle_date(self, date_spec):
    """ return True if the date matches the date_spec, otherwise return False """
    # date_test is a list of tuples:  [0] is the test for whether the test in [1]
    # should be applied to the date_spec parameter
    date_tests = [ ]

    date_tests.append(
      (
        lambda date_spec: re.match('daily', date_spec, re.IGNORECASE)
        , lambda date_spec: True # match every day
      )
    )

    for test in date_tests:
      if test[0](date_spec): return test[1](date_spec)

    return False # failed to match any test

  def format_tickle(self, message, indentation):
    """ return a formated tickle message, preserving original indentation """
    return indentation + message.strip() + "\n"

################################################################################

if __name__ == '__main__':
  Tickler()(sys.argv[1:])

# vim: set sw=2 ts=2:
