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
import re

class rule:
    def short_name(self):
        return "port checks"
    def long_name(self):
        return "Checks for open ports"
    def __init__(self, options):
        pass
    def analyze(self, options):
        check_results = [[],[],[],[],[]]
        out = os.popen('LC_ALL=C lsof -i -nP').read()
        services = {}
        # the regex need some improvement
        for i in re.finditer(r'([a-z0-9_-]+).*:([0-9]+) \(LISTEN\)', out):
            service_name = i.group(1)
            service_port = i.group(2)
            if service_name not in services:
                services[service_name] = [service_port]
            elif service_port not in services[service_name]:
                services[service_name].append(service_port)
        if len(services) > 0:
            for service in services:
                if len(services[service]) == 1:
                    tmp_msg = 'port "' + services[service][0] + '"'
                else:
                    tmp_msg = 'ports "' + '" and "'.join(services[service]) \
                        + '"'
                check_results[4].append('Service "' + service + '" using ' \
                    + tmp_msg + ' found')
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
