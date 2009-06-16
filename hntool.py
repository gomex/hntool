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

import hntool, getopt, sys, string, colors


# Functions
# Return all possible modules (rules)
def get_modules():	
	return hntool.__all__

# Show the usage help
def usage():
	print "Usage: " + sys.argv[0] + ' [options]'
	print "       -h, --help       : print this help"
	print "       -l, --list       : returns list of available rules"
	print "       -n, --nocolors   : does not use colors on output"
	sys.exit(2)


# get our options and process them
try:
	optlist, args = getopt.getopt(sys.argv[1:], "lhn:", ["list","help","nocolors"])
except getopt.GetoptError:
	usage()
	
use_colors = True

for i, k in optlist:	
	# Show all available modules (rules) and its description
	if i in ('-l','--list'):
		print "-"*20 + " hntool rule list " + "-"*20
		
		for module in get_modules():			
			print string.ljust(module, 20) + ": " + __import__('hntool.' + 
															   module, globals(), 
															   locals(), 
															   [hntool]).rule().long_name()
			
			
		sys.exit(2)
	
	if i in ('-n', '--nocolors'):
		use_colors = False
			
	
	if i in ('-h', '--help'):
		usage()

		
# Methods to show the check results
def msg_low_status(msg):
	if use_colors:
		return colors.colors.ENDC + '[ ' + colors.colors.LOW + 'LOW' + colors.colors.ENDC + ' ]    ' + msg
	else:
		return '[ LOW ]    ' + msg

def msg_medium_status(msg):
	if use_colors:
		return colors.colors.ENDC + '[ ' + colors.colors.WARNING + 'MEDIUM' + colors.colors.ENDC + ' ] ' + msg
	else:
		return '[ MEDIUM ] ' + msg

def msg_high_status(msg):
	if use_colors:
		return colors.colors.ENDC + '[ ' + colors.colors.HIGH + 'HIGH' + colors.colors.ENDC + ' ]   ' + msg		
	else:
		return '[ HIGH ]  ' + msg
		

# Run all the modules and its checks. The results of each module goes to "check_results"
for module in get_modules():
	check_results = [[],[],[]] # low, medium and high
	
	check_results = __import__('hntool.' + module ,globals(), locals(), [hntool]).rule().analyze()
	
	# Print all the results, from the 3 types of messages (low, medium and high).
	# First message is the "low" one (check_results[0]). The second one is
	# "medium" (check_results[1]) and the last one shows all "high" (check_results[2]) 
	# messages.
	if check_results[0] != []:
		for j in check_results[0]:
			print string.ljust(module, 20) + msg_low_status(j)
	if check_results[1] != []:
		for j in check_results[1]:
			print string.ljust(module, 20) + msg_medium_status(j) 
	if check_results[2] != []:
		for j in check_results[2]:
			print string.ljust(module, 20) + msg_high_status(j)

			