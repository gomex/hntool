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
		logindefs_file = '/etc/login.defs'
		inittab_file = '/etc/inittab'

		# Checks about the passwd file
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
				users_with_uid_zero = False # will be true if we find users with UID 0
				for user in users:
					# Checking if there's a user (other than root) that has UID 0
					if user[0] != 'root' and user[2] == '0':
						check_results[3].append('There is a user (not root) with UID 0')
						users_with_uid_zero = True

					# Checking if there's a user (other than root) with a valid shell
					if user[0] != 'root' and user[6] not in ['/sbin/nologin', '/bin/false', '/usr/bin/false']:
						check_results[2].append('User "' + user[0] + '" may have a harmful shell (' + user[6] + ')')
						
				if not users_with_uid_zero:
					check_results[0].append("There aren't users (not root) with UID 0")

			# Checking the permissions of the root home directory
			if os.path.exists('/root'):
				if oct(os.stat('/root')[stat.ST_MODE] & 0777) > 0750:
					check_results[2].append('Permissions on /root dir are greater than 700')

			passwd_fp.close()
			
			
		# Checks about the login.defs file
		if os.path.isfile(logindefs_file):
			logindefs_fp = open(logindefs_file,'r')
			
			# Getting only the lines that aren't commented or blank
			logindefs_lines = [x.strip('\n').split('\t') for x in logindefs_fp.readlines()
			                   if not (x[0].startswith('#') or not (x[0] != ''))]	
			
			# Getting only the line that starts with PASS_MAX_DAYS
			logindefs_lines = [x for i, x in enumerate(logindefs_lines) \
						if x[0].startswith('PASS_MAX_DAYS')]	
			
			# If PASS_MAX_DAYS is set to more than 90 day then we have a problem
			# logindefs_lines[0][1] == value of PASS_MAX_DAYS on the login.defs file
			if int(logindefs_lines[0][1]) > 90:
				check_results[2].append('By default passwords do not expires on 90 days or less')
			else:
				check_results[0].append('By default passwords expires on 90 days or less')
				
			logindefs_fp.close()
				
		# Checks about inittab file
		if os.path.isfile(inittab_file):
			inittab_fp = open(inittab_file, 'r')
			
			# Getting only the lines that aren't commented or blank
			inittab_lines = [x.strip('\n').split('\t') for x in inittab_fp.readlines()
			                   if not (x[0].startswith('#') or not (x[0] != ''))]
			
			
			if '~~:S:wait:/sbin/sulogin' in inittab_lines:
				check_results[0].append('Single-User Mode requires authentication')
			else:
				check_results[2].append('Single-User Mode does not requires authentication')
				
			inittab_fp.close()

		return check_results
	def type(self):
		return "config"
