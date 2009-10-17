#
# hntool rules - PostgreSQL
# Copyright (C) 2009 Sebastian SWC <mail@sebastianswc.net>
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
import shlex

class rule:
    def short_name(self):
        return "postgresql"
    def long_name(self):
        return "Check security problems on PostgreSQL configuration files"
    def analyze(self):
        check_results = [[],[],[],[],[]]
        pgsql_conf_file = ['/var/lib/pgsql/data/pg_hba.conf', '/var/lib/pgsql/data/postgresql.conf'] 
        
        
        postgresql_conf_file_found = False
        for pgsql_conf in pgsql_conf_file:
            if os.path.isfile(pgsql_conf):
                postgresql_conf_file_found = True
                try:
                    fp = open(pgsql_conf,'r')
                except IOError, (errno, strerror):
                    check_results[4].append('Could not open %s: %s' % (pgsql_conf, strerror))
                    continue

                # pg_hba.conf validation
                if 'pg_hba' in pgsql_conf:
                    for line in fp.readlines():
                        if line[0] != '#' and len(line.strip()) > 0:
                            line_conf = shlex.split(line)

                            # check unix sockets authentication
                            if line_conf[0] == 'local':
                                if 'trust' in line:
                                    check_results[2].append('Trusted local Unix authentication are allowed')
                                else:
                                    check_results[0].append('Trusted local Unix authentication are not allowed')

                            # check tcp/ip host authentication
                            if 'host' in line_conf[0]:
                                if 'trust' in line:
                                    check_results[3].append('Trusted connection on ' + line_conf[3] + ' are allowed')
                                else:
                                    check_results[0].append('Trusted connection on ' + line_conf[3] + ' are not allowed')

                elif 'postgresql' in pgsql_conf:
                    for line in fp.readlines():
						if len(line.strip()) > 0:
							line_conf = shlex.split(line)

							# check the default port
							if 'port =' in line:
								if '5432' in line:
									check_results[1].append('Server are running on default port (5432)')
								else:
									check_results[0].append('Server are not running at default port (5432)')
							# check sshl connections
							if 'ssl =' in line:
								if 'off' in line:
									check_results[1].append('Server are running without ssl connections support')
								else:
									check_results[0].append('Server are running with ssl connections support')


                fp.close()
                
        if not postgresql_conf_file_found:
            check_results[4].append('PostgreSQL configurations files are not found')


        return check_results
    def type(self):
        return "config"
