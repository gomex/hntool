# 
# hntool - output module - treminal
# Copyright (C) 2009 Authors
# Authors:
#   * Hugo Doria <mail@hugodoria.org>
#   * Aurelio A. Heckert <aurium ( a ) gmail dot com>
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   ( at your option ) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import hntool, string

class format:

  description = "Human friendly output for terminal"

  def __init__(self, options):
      options.add_option("-n", "--term_nocolors",
                         action="store_false",
                         dest="term_use_colors", default=True,
                         help="does not use colors on terminal output")

  def format_status( self, token ):
      use_colors = self.conf.term_use_colors
      if token == 'ok':
          return '[\033[1;92m   OK   \033[0m]' if use_colors else '[   OK   ]'
      elif token == 'low':
          return '[\033[1;30m  LOW   \033[0m]' if use_colors else '[  LOW   ]'
      elif token == 'medium':
          return '[\033[1;93m MEDIUM \033[0m]' if use_colors else '[ MEDIUM ]'
      elif token == 'high':
          return '[\033[1;91m  HIGH  \033[0m]' if use_colors else '[  HIGH  ]'
      elif token == 'info':
          return '[ \033[37m INFO \033[0m ]'   if use_colors else '[  INFO  ]'

  # Method to show the check results
  def msg_status( self, msg, status ):
    '''
    Method to show the check results
    '''
    maxmsg_len = hntool.util.term_len() - 15
    msg_splited = hntool.util.split_len( msg, maxmsg_len )
    result = ""
    i = 0
    while i < len(msg_splited) - 1:
      result += "   " + string.ljust( msg_splited[i], maxmsg_len ) + "\n"
      i += 1
    return result + "   " + \
           string.ljust( msg_splited[i], maxmsg_len ) + \
           self.format_status( status )

  def output( self, report, conf ):
    self.conf = conf
    # Print all the results, from the 5 types of messages ( ok, low, medium, high and info ).
    # First message is the "ok" one ( m['results'][0] ). The second one is
    # "low" ( m['results'][1] ). The third ( m['results'][2] ) is for "warnings"
    # and the fourth one is "high" ( m['results'][3] ), The last one is for
    # info messages.
    for m in report:
      print '\n' + m['title']
      if m['results'][0] != []:
        for result in m['results'][0]:
          print self.msg_status( result, 'ok' )
      if m['results'][1] != []:
        for result in m['results'][1]:
          print self.msg_status( result, 'low' )
      if m['results'][2] != []:
        for result in m['results'][2]:
          print self.msg_status( result, 'medium' )
      if m['results'][3] != []:
        for result in m['results'][3]:
          print self.msg_status( result, 'high' )
      if m['results'][4] != []:
        for result in m['results'][4]:
          print self.msg_status( result, 'info' )

