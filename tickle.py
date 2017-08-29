#!/usr/bin/env python3

import sys
import os
import argparse
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
        # echo line without modification
        if args.echo:
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

if __name__ == '__main__':
  main(sys.argv[1:])

# vim: set sw=2 ts=2:
