# $Id$
#
# Copyright (c) 2005 Matt Behrens.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Support for Datel's Action Replay MAX for DS image files
"""

WILDCARD = "Action Replay MAX for DS uncompressed save files(*.duc)|*.duc"

import codecs

def nullpad(s, width):
    """
    Pad a string with NULs to a given width
    """

    s = s + "\x00" * (width - len(s))
    return s[:width]

class SaveFile(object):
    """
    Action Replay MAX for DS save image file (.dss)
    """

    def __init__(self, file, save_class):
        self._magic = file.read(16)

        if self._magic != "ARDS000000000001":
            raise ValueError, "magic not found in save file"

        # These look like NUL-padded UTF-16; cross your fingers
        self.game_name = (codecs.BOM_UTF16_LE +
                file.read(64)).decode("utf-16")
        self.save_name = (codecs.BOM_UTF16_LE +
                file.read(64)).decode("utf-16")
        self.description = (codecs.BOM_UTF16_LE +
                file.read(126)).decode("utf-16")

        # Remainder of header is currently opaque to us; there appear to be
        # ASCII copies of the text data later but it is unused by the
        # user interface and unpredictable
        self._opaque = file.read(230)

        if len(self._magic) != 16 or \
                len(self.game_name) != 32 or \
                len(self.save_name) != 32 or \
                len(self.description) != 63 or \
                len(self._opaque) != 230:
            raise IOError, "short read"

        self.game_name = self.game_name.rstrip("\x00")
        self.save_name = self.save_name.rstrip("\x00")
        self.description = self.description.rstrip("\x00")

        # Remainder of file is the actual save
        self.save = save_class(file)

    def write(self, file):
        """
        Write the save image to a file
        """

        file.write(self._magic)

        # Write UTF-16-encoded strings with the byte order marker removed
        file.write(nullpad(self.game_name,
            32).encode("utf-16")[len(codecs.BOM_UTF16_LE):])
        file.write(nullpad(self.save_name,
            32).encode("utf-16")[len(codecs.BOM_UTF16_LE):])
        file.write(nullpad(self.description,
            63).encode("utf-16")[len(codecs.BOM_UTF16_LE):])

        file.write(self._opaque)

        self.save.write(file)

# ex:et:sw=4:ts=4
