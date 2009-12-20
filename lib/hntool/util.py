# 
# hntool - utility functions
# Copyright (C) 2009 Hugo Doria <mail@hugodoria.org>
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# 

import os
import sys
import re

# Functions

# Show the usage help
def usage():
    '''Method to show the usage help'''
    print "Usage: " + sys.argv[0] + ' [options]'
    print "       -h, --help	: print this help"
    print "       -l, --list	: returns list of available rules"
    print "       -n, --nocolors	: does not use colors on output"
    print "       -t, --output_type	: select the output format"
    sys.exit(2)

def is_root():
    '''Method to check if hntool is running as root.'''		
    if os.getuid() == 0:
        return True

def is_unix():
    '''Method to check if we have power'''
    if os.name == 'posix':
        return True
    return False

def term_len():
    return int(os.popen('stty size', 'r').read().split()[1])

def split_len(seq, length):
    result = []
    p = re.compile("(.{,"+str(length)+"})\s")
    while len(seq) > 0:
        if len(seq) < length:
            result.append(seq)
            break
        else:
            tmp,seq = (p.split(seq,1))[1:]
            result.append(tmp)
    return result

