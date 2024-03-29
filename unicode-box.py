#!/usr/bin/env python2
# coding: utf-8

from __future__ import print_function
import sys
from collections import namedtuple

BoxChars = namedtuple('BoxChars', [
   'horiz', 'vert',
   'topleft', 'topright', 'botleft', 'botright',
   'midleft', 'midright', 'topmid', 'botmid', 'mid'
])

chars_single = BoxChars(*u'─│┌┐└┘├┤┬┴┼')

def field_width(data, n):
   width = 0
   for row in data:
      thisWidth = row[n:n+1]
      if thisWidth:
         thisWidth = len(str(thisWidth[0]))
         if thisWidth > width:
            width = thisWidth
   return width

class Converter(object):
   def __init__(self, chars):
      self.chars = chars
      self._xpadding = 0

   def xpadding(self, *args):
      if len(args) == 1:
         self._xpadding = int(args[0])
      elif not args:
         return self._xpadding
      else:
         raise ValueError

   def convert(self, data):
      widths = [field_width(data, n) for n in xrange(len(data[0]))]
      res = u''
      for n, row in enumerate(data):
         if n == 0:
            res += self.draw_rule('top', widths) + u'\n'
         else:
            res += self.draw_rule('mid', widths) + u'\n'
         res += self.draw_data_row(widths, row) + u'\n'
      res += self.draw_rule('bot', widths) + u'\n'
      return res

   def draw_rule(self, pos, widths):
      if pos == 'top':
         ch = (self.chars.horiz, self.chars.topleft, self.chars.topright, self.chars.topmid)
      elif pos == 'bot':
         ch = (self.chars.horiz, self.chars.botleft, self.chars.botright, self.chars.botmid)
      elif pos == 'mid':
         ch = (self.chars.horiz, self.chars.midleft, self.chars.midright, self.chars.mid)
      else:
         raise ValueError

      res = u''
      for n, width in enumerate(widths):
         if n == 0:
            res += ch[1]
         else:
            res += ch[3]
         res += ch[0] * (width + 2 * self._xpadding)
      res += ch[2]

      return res

   def draw_data_row(self, widths, row):
      res = self.chars.vert
      for n, width in enumerate(widths):
         res += u'{pad}{0:{width}}{pad}{1}'.format(row[n], self.chars.vert, width=width, pad=u' '*self._xpadding)
      return res

def parse_args(args, rowsep=';'):
   data = []
   row = []

   for arg in args:
      if arg == rowsep:
         data.append(row)
         row = []
      else:
         row.append(arg)

   if row:
      data.append(row)

   return data

if __name__ == '__main__':
   c = Converter(chars_single)
   c.xpadding(1)

   # Example
   # s = c.convert([
   #    ['...', 'aaa', 'bbb'],
   #    ['...', 'aaa', 'bbb']
   # ])

   s = c.convert(parse_args(sys.argv[1:], ';'))

   print(s.encode('utf-8'))

# TODO
# ====
#
#  * Command line args for setting:
#     - padding
#     - charset
#     - row separator
#     - transpose
#
#  * Create a more descriptive name than Converter
#
#  * Check bounds (check if all rows are the same size). Currently an
#  ugly exception is thrown.
#
#  * Empty cells (they have no border of themselves, only the ones that
#  are implied by the neighboring cells). Implement them and add some
#  way to specify them at the command line. There should be a command
#  line arg for it too.

