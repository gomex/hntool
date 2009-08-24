#
# hntool rules - authentication
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
import stat

class rule:
	def short_name(self):
		return "authentication"
	def long_name(self):
		return "Checks users, groups and authentications"
	def analyze(self):
		check_results = [[],[],[],[],[]]
		passwd_file = '/etc/passwd'
		shadow_file = '/etc/shadow'

		if os.path.isfile(passwd_file):
			# Gets the values of each line of the passwd file
			passwd_fp = open(passwd_file,'r')
			users = [x.strip('\n').split(':') for x in passwd_fp.readlines()]

			users = [x for i, x in enumerate(users) \
						if not (x[0].startswith('#') or not (x[0] != ''))]
			for indexc, line in enumerate(users):
				for indexv, col in enumerate(line):
					users[indexc][indexv] = col.strip()

			if users:
				for user in users:
				# Checking if there's a user (other than root) that has UID 0
					if user[0] != 'root' and user[2] == '0':
						check_results[3].append('There is a user (not root) with UID 0')

					# Checking if there's a user (other than root) with a valid shell
					if user[0] != 'root' and user[6] not in ['/sbin/nologin', '/bin/false', '/usr/bin/false']:
						check_results[2].append('User "' + user[0] + '" may have a harmful shell (' + user[6] + ')')

			# Checking the permissions of the root home directory
			if os.path.exists('/root'):
				if oct(os.stat('/root')[stat.ST_MODE] & 0777) > 0750:
					check_results[2].append('Permissions on /root dir are greater than 700')

			passwd_fp.close()


		return check_results
	def type(self):
		return "config"
