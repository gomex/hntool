#
# hntool rules - port checks
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

import os

class rule:
	def short_name(self):
		return "port checks"
	def long_name(self):
		return "Checks for open ports"
	def analyze(self):
		check_results = [[],[],[],[],[]]
		
		# Checking for old files in /tmp
		netstat_results = os.popen('LC_ALL="en_US" netstat -tulpan | grep LISTEN')
		netstat_results = [res for res in netstat_results.readlines()]

		if len(netstat_results) > 0:
			lines = [ filter(None,netstat_results[indexc].split(' ')) \
		                for indexc, item in enumerate(netstat_results) ]

			for indexc, item in enumerate(lines):
				port = lines[indexc][3].split(':')[1]
				service = lines[indexc][6].split('/')
				if len(service) == 1: service = service[0]
				else: service = service[1].rstrip()
				check_results[4].append('Service "' + service + '" ' + \
																'using port "' + port + '" found')

		else:
			check_results[0].append("There's no ports opened")

		device_list = ['/dev/null', '/dev/tty', '/dev/console']
		exec_device = False
		for device in device_list:
			if os.path.lexists(device):
				if os.access(device ,os.X_OK):
					check_results[3].append('Found device "' + device + '" with executable rights')
					exec_device = True
		if not exec_device:
			check_results[1].append('Devices without executable rights')

		return check_results
	def type(self):
		return "config"
