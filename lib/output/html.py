# 
# hntool - output module - html
# Copyright ( C ) 2009 Authors
# Authors:
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

  def format_status( self, token ):
      if token == 'ok':
          return '<td align="center" bgcolor="#00ff00">   OK   </td>'
      elif token == 'low':
          return '<td align="center" bgcolor="#888888">  LOW   </td>'
      elif token == 'medium':
          return '<td align="center" bgcolor="#ffff00"> MEDIUM </td>'
      elif token == 'high':
          return '<td align="center" bgcolor="#ff0000">  HIGH  </td>'
      elif token == 'info':
          return '<td align="center" bgcolor="#0000ff">  INFO  </td>'

  # Method to show the check results
  def msg_status( self, msg, status ):
    '''
    Method to show the check results
    '''
    return '<tr>' + \
           self.format_status( status ) + \
           '<td>' + msg + '</td>' + \
           '</tr>'

  def output( self, report, conf ):
    self.conf = conf
    # Print all the results, from the 5 types of messages ( ok, low, medium, high and info ).
    # First message is the "ok" one ( m['results'][0] ). The second one is
    # "low" ( m['results'][1] ). The third ( m['results'][2] ) is for "warnings"
    # and the fourth one is "high" ( m['results'][3] ), The last one is for
    # info messages.
    print '<html><body><div align="center">'
    print '<table border="0">'
    for m in report:
      print '<tr><th colspan="2" align="center">' + m['title'] + '</th></tr>'
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
    print '</table></div></body></html>'

