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

import hntool, getopt, sys, string

# Functions
# Return all possible modules (rules)
def get_modules():
	return hntool.__all__

# Show the usage help
def usage():
	print "Usage: " + sys.argv[0]
	print "       -l    : returns list of available rules"	
	sys.exit(2)

	
# get our options and process them
try:
	optlist, args = getopt.getopt(sys.argv[1:], "lh:", ["list","help"])
except getopt.GetoptError:
	usage()
	
	
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
			
			
# Run all the modules and its checks. The results of each module goes to "check_results"
for module in get_modules():
	check_results = [[],[],[]] # info, warning and error
	
	check_results = __import__('hntool.' + module ,globals(), locals(), [hntool]).rule().analyze()
	
	# Print all the results, from the 3 types of messages (info, warning and error).
	# First message is the "info" one (check_results[0]). The seconde one is
	# "warning" (check_results[1]) and the last one shows all "errors" (check_results[2]) 
	# messages.
	if check_results[0] != []:
		for j in check_results[0]:
			print string.ljust(module, 10) + " I: " + j
	if check_results[1] != []:
		for j in check_results[1]:
			print string.ljust(module, 10) + " W: " + j
	if check_results[2] != []:
		for j in check_results[2]:
			print string.ljust(module, 10) + " E: " + j

	