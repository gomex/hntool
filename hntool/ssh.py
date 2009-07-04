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

import os

class rule:
	def short_name(self):
		return "ssh"
	def long_name(self):
		return "Checks security problems on sshd config file"
	def analyze(self):
		check_results = [[],[],[],[]]
		ssh_conf_file = '/etc/ssh/sshd_config'
		
		if os.path.isfile(ssh_conf_file):
			fp = open(ssh_conf_file,'r') 
			lines = [x.strip('\n') for x in fp.readlines()]
			
			# Checking if SSH is using the default port
			if 'Port 22' in lines or '#Port 22' in lines:					
				check_results[1].append('SSH is using the default port')
			else:
				check_results[0].append('SSH is not using the default port')
				
			# Checking if the Root Login is allowed	
			if 'PermitRootLogin yes' in lines or '#PermitRootLogin' in lines:
				check_results[1].append('Root access allowed!')
			else:
				check_results[0].append('Root access is not allowed!')
          
			# Checking if SSH is using protocol v2 (recommended)
			if 'Protocol 2' not in lines:    
				check_results[1].append('SSH is not using protocol v2')
			else:
				check_results[0].append('SSH is using protocol v2')
				
			# Checking if empty password are allowed (shouldn't)
			if 'PermitEmptyPasswords yes' in lines:
				check_results[2].append('Empty passwords are allowed')
			else:
				check_results[0].append('Empty passwords are not allowed')
        
			# Checking if X11 Forward is allowed (shouldn't)
			if 'X11Forwarding yes' in lines:
				check_results[1].append('X11 forward is allowed')
			else:
				check_results[0].append('X11 forward is not allowed')
        
			# Checking if SSH allow TCP Forward (shouldn't)
			if 'AllowTcpForwarding yes' in lines:
				check_results[1].append('TCP forwarding is allowed')
			else:
				check_results[0].append('TCP forwarding is not allowed')
				
			# Closing the sshd_config file
			fp.close()
					
		return check_results
	def type(self):
		return "config"