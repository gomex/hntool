# 
# hntool - output module - treminal
# Copyright ( C ) 2009 Authors
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

  def color_ok( self ):
      return '[\033[1;92m   OK   \033[0m]'

  def color_low( self ):
      return '[\033[1;30m  LOW   \033[0m]'

  def color_medium( self ):
      return '[\033[1;93m MEDIUM \033[0m]'

  def color_high( self ):
      return '[\033[1;91m  HIGH  \033[0m]'

  def color_info( self ):
      return '[ \033[37m INFO \033[0m ]'

  # Method to show the check results
  def msg_status( self, msg, status ):
    '''
    Method to show the check results
    '''
    if self.conf['use_colors']:
      if status == 'ok':
        return string.ljust( msg, 70 ) + hntool.util.color_ok( )
      elif status == 'low':
        return string.ljust( msg, 70 ) + hntool.util.color_low( )
      elif status == 'medium':
        return string.ljust( msg, 70 ) + hntool.util.color_medium( )
      elif status == 'high':
        return string.ljust( msg, 70 ) + hntool.util.color_high( )
      elif status == 'info':
        return string.ljust( msg, 70 ) + hntool.util.color_info( )

    else:
      if status == 'ok':
        return string.ljust( msg, 70 ) + '[   OK   ]'
      elif status == 'low':
        return string.ljust( msg, 70 ) + '[  LOW   ]'
      elif status == 'medium':
        return string.ljust( msg, 70 ) + '[ MEDIUM ]'
      elif status == 'high':
        return string.ljust( msg, 70 ) + '[  HIGH  ]'
      elif status == 'info':
        return string.ljust( msg, 70 ) + '[  INFO  ]'  

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
          print '   ' + self.msg_status( result, 'ok' )
      if m['results'][1] != []:
        for result in m['results'][1]:
          print '   ' + self.msg_status( result, 'low' )
      if m['results'][2] != []:
        for result in m['results'][2]:
          print '   ' + self.msg_status( result, 'medium' )
      if m['results'][3] != []:
        for result in m['results'][3]:
          print '   ' + self.msg_status( result, 'high' )
      if m['results'][4] != []:
        for result in m['results'][4]:
          print '   ' + self.msg_status( result, 'info' )

