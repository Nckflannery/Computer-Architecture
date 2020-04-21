#!/usr/bin/env python3

"""Main."""

import os
import sys
from cpu import *
'''
Usage:

python(3) ls8.py call -> loads ../examples/call.ls8 into cpu
'''
# Gets current working directory and appends \examples\
# So we don't need to type it every time
current_dir = os.getcwd() + '\examples\\'

# Combines CL argument with cwd and appends .ls8
# So we don't need to type it every time
command = current_dir + sys.argv[1] + '.ls8'
print(command)
cpu = CPU()

cpu.load(command)
cpu.run()