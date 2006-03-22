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
Support for M3 Adapter save files (.dat)
"""

WILDCARD = "M3 Adapter save files (*.dat)|*.dat"

class SaveFile(object):
    """
    M3 Adapter save file (.dss)
    """

    def __init__(self, file, save_class):
        # File leads off with actual save
        self.save = save_class(file)

        # Remainder of file is opaque footer
        self._opaque = file.read(1024)

        if len(self._opaque) != 1024:
            raise IOError, "short read"

    def write(self, file):
        """
        Write the save image to a file
        """

        self.save.write(file)
        file.write(self._opaque)

# ex:et:sw=4:ts=4
