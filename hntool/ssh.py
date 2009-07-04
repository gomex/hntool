# 
# hntool rules - ssh
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

import os, ConfigParser

class rule:
	def short_name(self):
		return "ssh"
	def long_name(self):
		return "Checks security problems on sshd config file"
	def analyze(self):
		check_results = [[],[],[]]
		ssh_conf_file = '/etc/ssh/sshd_config'
		
		if os.path.isfile(ssh_conf_file):
			fp = open(ssh_conf_file,'r')
			
			for line in fp:
				
				if line.startswith('Port 22') or line.startswith('#Port 22'):					
					check_results[0].append('SSH is using the default port')
					
				if line.startswith('PermitRootLogin yes') or line.startswith('#PermitRootLogin'):					
					check_results[1].append('Root access allowed!')
					
				if line.startswith('Protocol'):					
					if not line.startswith('Protocol 2'):		
						check_results[1].append('SSH is not using protocol v2')
						
				if line.startswith('PermitEmptyPasswords yes'):
					check_results[2].append('Empty passwords are allowed')
				
				if line.startswith('X11Forwarding yes'):
					check_results[1].append('X11 forward is allowed')
				
				if line.startswith('AllowTcpForwarding yes'):
					check_results[1].append('TCP forwarding is allowed')
						
			fp.close()
					
		return check_results
	def type(self):
		return "config"