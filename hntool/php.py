#
# hntool rules - php
# Copyright (C) 2009 Candido Vieira <cvieira.br@gmail.com>
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

""" This rules are based on Mad Irish PHP Security tips: http://www.madirish.net/?article=229"""

import os

class rule:
    def short_name(self):
        return "php"
    def long_name(self):
        return "Checks security problems on php config file"
    def analyze(self):
        check_results = [[],[],[],[],[]]
        conf_files = ['/etc/php5/apache2/php.ini', '/etc/php5/cli/php.ini', '/etc/php.ini'] 

        for php_conf in conf_files:
            if os.path.isfile(php_conf):
                
                try:
                    fp = open(php_conf,'r')
                except IOError, (errno, strerror):
                    check_results[4].append('Could not open %s: %s' % (sshd_conf, strerror))
                    continue

                lines = [x.strip('\n').lower() for x in fp.readlines()]

                if 'register_globals = on' in lines:
                    check_results[3].append('Register globals is on')
                else:
                    check_results[0].append('Register globals is off')
                
                if 'safe_mode = on' in lines:
                    check_results[1].append('Safe mode is on (fake security)')
                else:
                    check_results[4].append('Safe mode is off')
                
                if 'display_errors = on' in lines:
                    check_results[1].append('Display errors is on')
                else:
                    check_results[0].append('Display errors is  off')
                
                fp.close()

        return check_results
    def type(self):
        return "file"
