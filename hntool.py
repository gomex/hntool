#! /usr/bin/env python
#
# hntool - A hardening tool for Linux/BSD
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

import hntool.util
import getopt
import hntool
import string
import sys
import os


# Functions
def is_root():
	'''Method to check if hntool is running as root.'''		
	if os.getuid() == 0:
		return True		

# Return all possible modules (rules)
def get_modules():
	'''Method to return all modules available'''
	return hntool.__all__

def is_unix():
	'''Method to check if we have power'''
	if os.name == 'posix':
		return True
	return False

# Show the usage help
def usage():
	'''Method to show the usage help'''
	print "Usage: " + sys.argv[0] + ' [options]'
	print "       -h, --help	: print this help"
	print "       -l, --list	: returns list of available rules"
	print "       -n, --nocolors	: does not use colors on output"
	sys.exit(2)


# vars
use_colors = True # using colors by default
hntool_version = 0.1

# yes, only unix for now
if not is_unix():
	print 'Error: You must have a Unix(-like) box. (No candy for you)'
	sys.exit(2)

# checking if we are root. we need to be. oh yeah, baby.
if not is_root():
	print 'Error: You must be root to run hntool'
	print
	print usage()
	sys.exit(2)

# get our options and process them
try:
	optlist, args = getopt.getopt(sys.argv[1:], "lhn", ["list","help","nocolors"])
except getopt.GetoptError:
	usage()

for i, k in optlist:
	# Show all available modules (rules) and its description
	if i in ('-l','--list'):
		print "-"*20 + " hntool rule list " + "-"*20

		for module in get_modules():
			print string.ljust(module, 20) + ": " + __import__('hntool.' + \
					module, globals(), locals(), [hntool]).rule().long_name()

		sys.exit(2)

	# do not use colors
	if i in ('-n', '--nocolors'):
		use_colors = False

	# show help
	if i in ('-h', '--help'):
		usage()


# Method to show the check results
def msg_status(msg, status):
	'''
	Method to show the check results
	'''
	if use_colors:
		if status == 'ok':
			return string.ljust(msg,70) + hntool.util.color_ok()
		elif status == 'low':
			return string.ljust(msg,70) + hntool.util.color_low()
		elif status == 'medium':
			return string.ljust(msg,70) + hntool.util.color_medium()
		elif status == 'high':
			return string.ljust(msg,70) + hntool.util.color_high()
		elif status == 'info':
			return string.ljust(msg,70) + hntool.util.color_info()

	else:
		if status == 'ok':
			return string.ljust(msg,70) + '[   OK   ]'
		elif status == 'low':
			return string.ljust(msg,70) + '[  LOW   ]'
		elif status == 'medium':
			return string.ljust(msg,70) + '[ MEDIUM ]'
		elif status == 'high':
			return string.ljust(msg,70) + '[  HIGH  ]'
		elif status == 'info':
			return string.ljust(msg,70) + '[  INFO  ]'	


print '[ Starting hntool checks ]'

# Run all the modules and its checks. The results of each module goes to "check_results"
for module in get_modules():
	check_results = [[],[],[],[],[]] # ok, low, medium, high and info

	# Getting all results from the check and the module/check description
	check_results = __import__('hntool.' + module ,globals(), locals(), [hntool]).rule().analyze()
	check_description = __import__('hntool.' + module ,globals(), locals(), [hntool]).rule().long_name()

	# Prints the module description
	print '\n' + check_description

	# Print all the results, from the 5 types of messages (ok, low, medium, high and info).
	# First message is the "ok" one (check_results[0]). The second one is
	# "low" (check_results[1]). The third (check_results[2]) is for "warnings"
	# and the fourth one is "high" (check_results[3]), The last one is for
	# info messages.
	if check_results[0] != []:
		for j in check_results[0]:
			print '   ' + msg_status(j, 'ok')
	if check_results[1] != []:
		for j in check_results[1]:
			print '   ' + msg_status(j, 'low')
	if check_results[2] != []:
		for j in check_results[2]:
			print '   ' + msg_status(j, 'medium')
	if check_results[3] != []:
		for j in check_results[3]:
			print '   ' + msg_status(j, 'high')
	if check_results[4] != []:
		for j in check_results[4]:
			print '   ' + msg_status(j, 'info')
