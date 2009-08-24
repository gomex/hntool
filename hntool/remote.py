#
# hntool rules - remote access
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
		return "remote access"
	def long_name(self):
		return "Checks for remote access allowed"
	def analyze(self):
		check_results = [[],[],[],[],[]]
		hosts_allow_file = '/etc/hosts.allow'
		hosts_deny_file  = '/etc/hosts.deny'

		if os.path.isfile(hosts_deny_file):
			fp = open(hosts_deny_file, 'r')
			lines = [x.strip('\n').split(':') for x in fp.readlines()]

			#check access in hosts.allow and remove comments and whitespaces
			all_access = [srv for srv in lines]
			all_access = [x for i, x in enumerate(all_access) \
							if not (x[0].startswith('#') or not x[0] != '')]
			for indexc, line in enumerate(all_access):
				for indexv, col in enumerate(line):
					all_access[indexc][indexv] = col.strip()

			if all_access:
				for index, service in enumerate(all_access):
					#specific service with all access
					if (service[0] == 'ALL' and \
							service[1] == 'ALL' and \
							service[2] == 'DENY'):
						check_results[0].append('Default policy is deny any remote access')
			else:
				check_results[1].append('Not found a default policy')
			#closing file
			fp.close()


		if os.path.isfile(hosts_allow_file):
			fp = open(hosts_allow_file,'r')
			all_access = [x.strip('\n').split(':') for x in fp.readlines()]

			#check access in hosts.allow and remove comments and whitespaces
			all_access = [x for i,x in enumerate(all_access) \
							if not (x[0].startswith('#') or not (x[0] != ''))]
			for indexc, line in enumerate(all_access):
				for indexv, col in enumerate(line):
					all_access[indexc][indexv] = col.strip()

			if all_access:
				for index, service in enumerate(all_access):
					#specific service with all access
					if service[0] != 'ALL' and service[1] == 'ALL':
						check_results[2].append('Service "' + service[0] + \
								'" with all remote access')
					#specific service with all access
					elif service[0] != 'ALL' and service[1] != 'ALL':
						check_results[2].append('Service "' + service[0] + \
								'" with remote access from "' + service[1] + '"')
					#any service to specific address
					elif service[0] == 'ALL' and service[1] != 'ALL':
						check_results[2].append('Any service are with remote access from "' + service[1] + '"')
					#any service with all access
					elif service[0] == 'ALL' and service[1] == 'ALL':
						check_results[3].append('Any service are with all remote access')
			#closing file
			fp.close()
		else:
			check_results[0].append('Did not found services with all remote access')

		return check_results

