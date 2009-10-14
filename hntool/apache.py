#
# hntool rules - apache
# Copyright (C) 2009 Rafael Gomes <rafaelgomes@techfree.com.br>
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

# To do : Include code to check when sintax that there isn't in conf

import os

class rule:
    def short_name(self):
        """ Returns a short name used on help """
        return "apache"

    def long_name(self):
        """ Returns a module description used on report """
        return "Checks security problems on Apache config file"

    def analyze(self):
        """ Analyze Apache config file searching for harmful settings"""
        check_results = [[],[],[],[],[]]
        apache_conf_files = ['/etc/httpd/conf/httpd.conf', '/etc/apache2/conf.d/security', '/etc/apache2/apache2.conf'] 

        for apache_conf in apache_conf_files:
            if os.path.isfile(apache_conf):
                try:
                    fp = open(apache_conf,'r')
                except IOError, (errno, strerror):
                    check_results[4].append('Could not open %s: %s' % (apache_conf, strerror))
                    continue

                lines = [x.strip('\n') for x in fp.readlines()]

                # Checking if ServerTokens is using harmful conf
                if not 'ServerTokens Minimal' in lines:
                    check_results[0].append('ServerTokens is not using harmful conf')				
                else:			
                    check_results[2].append('ServerTokens is using harmful conf (set Minimal)')

                # Checking if KeepAlive is set to On			
                if 'KeepAlive On' in lines:			
                    check_results[0].append('KeepAlive is not using harmful conf')
                else:
                    check_results[2].append('KeepAlive is using harmful conf (set On)')

                # Checking if KeepAlive is set to On			
                if 'ServerSignature Off' in lines:			
                    check_results[0].append('ServerSignature is not using harmful conf')
                else:
                    check_results[2].append('ServerSignature is using harmful conf (set Off)')

                # Checking if LimitRequestBody is bigger than 0		
                if 'LimitRequestBody' in lines:			
                    for line in lines: 
                        if line.startswith('LimitRequestBody') is True:
                            piece = line.split(' ')
                            if int(piece[1]) == 0:
                                check_results[0].append('LimitRequestBody is not using harmful value (0)')
                            else:
                                check_results[2].append('LimitRequestBody is using harmful value (0)')

                # Checking Timeout less than 300
                tvalue = 300			
                for line in lines: 
                    if line.startswith('Timeout') is True:
                        piece = line.split(' ')
                        if int(piece[1]) <= tvalue:
                            check_results[0].append('Timeout is not using harmful value (>=%s)' % (tvalue))
                        else:
                            check_results[2].append('Timeout is using harmful value (>=%s)' % (tvalue))		   

                # Closing the apache_config file
                fp.close()

        return check_results    
    def type(self):
        return "config"
