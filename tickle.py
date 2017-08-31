#!/usr/bin/env python3

import sys
import os
import argparse
import re
from tempfile import mkstemp
from shutil import copystat

################################################################################

def main(argv):
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
        sys.stdout.write(process_tickle(line))
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

################################################################################

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

def process_tickle(line):
  # determine if line is a tickle
  # if so, determine if the tickle matches today 
  # if so, return a formated message
  m = tickle_regex.match(line)
  if m:
    indent = m.group('indent')
    date_spec = m.group('date_spec')
    if date_spec: 
      date_spec = date_spec.lower()
    else:
      # if no date specification, default to daily
      date_spec = 'daily'
    message = m.group('message')

    if date_spec == 'daily':
      return format_tickle(m.group('message'), m.group('indent'))
  else:
    return ''

def format_tickle(message, indentation):
  # return a formated tickle message, preserving original indentation
  return indentation + message.strip() + "\n"

################################################################################

if __name__ == '__main__':
  main(sys.argv[1:])

# vim: set sw=2 ts=2:
