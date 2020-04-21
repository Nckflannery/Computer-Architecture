#!/usr/bin/env python3

"""Main."""

import os
import sys
from cpu import *
'''
Usage:

python(3) ls8.py call -> loads ../examples/call.ls8 into cpu

To load new programs, add program file to /examples folder
'''
# Gets current working directory and appends \examples\
# So we don't need to type it every time
current_dir = os.getcwd() + '\examples\\'

# Combines CL argument with cwd
# So we don't need to type it every time
if sys.argv[1][-4] == '.':
    # Checks if CL args have a file type included (i.e. '.txt')
    # allowing users to use programs not ending in ls8
    command = current_dir + sys.argv[1]
else:
    # If not, add .ls8 by default
    command = current_dir + sys.argv[1] + '.ls8'

cpu = CPU()

cpu.load(command)
cpu.run()