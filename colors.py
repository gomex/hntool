# 
# hntool - A hardening tool for Linux/BSD
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
# 

class colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[1;92m'
    LOW = '\033[1;30m'
    WARNING = '\033[1;93m'
    HIGH = '\033[1;91m'
    ENDC = '\033[0m'
    INFO = '\033[37m'

    def disable(self):
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.LOW = ''
        self.WARNING = ''
        self.HIGH = ''
        self.ENDC = ''
        self.INFO = ''
