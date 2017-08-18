#!/usr/bin/env python

import sys
import os
import getopt

USAGE = 'tickle <tickler_file> [<tickler_file2> ... <tickler_fileN>]'

################################################################################

def main(argv):
  try:
    opts, args = getopt.getopt(argv, '', [])
  except getopt.GetoptError:
    print USAGE
    sys.exit(2)

  if len(args) == 0:
    print USAGE
    
  for filename in args:
    if os.access(filename, os.R_OK):
      tickler_file = open(filename, 'r')
      for line in tickler_file:
        # echo line without modification
        sys.stdout.write(line)
      tickler_file.close()

################################################################################

if __name__ == '__main__':
  main(sys.argv[1:])

# vim: set sw=2 ts=2:
