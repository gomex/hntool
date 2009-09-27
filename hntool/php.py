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

""" This module implements rules to check security on PHP config files. \
Most of rules were written based on Mad Irish PHP Security tips: http://www.madirish.net/?article=229
"""


import os
import ConfigParser

class rule:
    def short_name(self):
        """ Returns a short name used on help """
        return "php"
    
    def long_name(self):
        """ Returns a module description used on report """
        return "Checks security problems on php config file"
    
    def analyze(self):
        """ Analyze PHP config file searching for harmful settings"""
        check_results = [[],[],[],[],[]]
        conf_files = ['/etc/php5/apache2/php.ini', '/etc/php5/cli/php.ini', '/etc/php.ini'] 

        for php_conf in conf_files:
            if os.path.isfile(php_conf):                
                config = ConfigParser.ConfigParser()
                
                try:
                    config.read(php_conf)
                except ConfigParser.ParsingError, (errno, strerror):
                    check_results[4].append('Could not parse %s: %s' % (php_conf, strerror))
                    continue
                
                if not config.has_section('PHP'):
                    check_results[4].append('%s is not a PHP config file' % (php_conf))
                    continue
                
                if config.has_option('PHP', 'register_globals'):
                    rg = config.get('PHP', 'register_globals').lower()
                    if rg == 'on':
                        check_results[3].append('Register globals is on')
                    elif rg == 'off':
                        check_results[0].append('Register globals is off')
                    else:
                        check_results[4].append('Unknown value for register globals')
                else:
                    check_results[4].append('Register globals not found')
                
                if config.has_option('PHP', 'safe_mode'):
                    sm = config.get('PHP', 'safe_mode').lower()
                    if sm == 'on':
                        check_results[1].append('Safe mode is on (fake security)')
                    elif sm == 'off':
                        check_results[4].append('Safe mode is off')
                    else:
                        check_results[4].append('Unknown value for safe mode')
                else:
                    check_results[4].append('Safe mode not found')
                
                if config.has_option('PHP', 'display_errors'):
                    de = config.get('PHP', 'display_errors').lower()
                    if de == 'on':
                        check_results[2].append('Display errors is on (stdout)')
                    elif de == 'off':
                        check_results[0].append('Display errors is off')
                    elif de == 'stderr':
                        check_results[4].append('Display errors set to stderr')
                    else:
                        check_results[4].append('Unknown value for display errors')
                else:
                    check_results[4].append('Display errors not found')
                
                if config.has_option('PHP', 'expose_php'):
                    ep = config.get('PHP', 'expose_php').lower()
                    if ep == 'on':
                        check_results[1].append('Expose PHP is on')
                    elif ep == 'off':
                        check_results[0].append('Expose PHP is off')
                    else:
                        check_results[4].append('Unknown value for expose PHP')
                else:
                    check_results[4].append('Expose PHP not found')
                

        return check_results
    def type(self):
        return "file"
