# 
# hntool rules - filesystems
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

import hntool
import os

class rule:
	def short_name(self):
		return "filesystems"
	def long_name(self):
		return "Checks filesystems for security problems"
	def analyze(self):
		check_results = [[],[],[],[]]
		locate_database = '/var/lib/mlocate/mlocate.db'
		
		# Checking if the locate database exists
		if not os.path.isfile(locate_database):
			check_results[1].append('mlocate.db not found. Run updatedb.')
		else:
			check_results[0].append('mlocate.db found')
        
		if os.getenv('USER') == 'root':
			# Checking for old files in /tmp
			find_results = os.popen('find /tmp -type f -atime +30')
			if len(find_results.readlines()) > 0:
				check_results[1].append('Found old files (+30 days) in /tmp')
			else:
				check_results[0].append('Did not found old files (+30 days) in /tmp')
		
		return check_results
	def type(self):
		return "files"