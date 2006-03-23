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
Daigasso! Band Brothers DS save manipulation
"""

import nincodec

GAME_DATA_SIZE = 0x800
GAME_DATA_BLOCK_SIZE = 0x8000
SCORE_SIZE = 0x6000
PADDING_SIZE = 0x8000

class GameData(object):
    """
    Daigasso! Band Brothers game data
    """

    def __init__(self, file):
        self.data = file.read(GAME_DATA_BLOCK_SIZE)
        if len(self.data) != GAME_DATA_BLOCK_SIZE:
            raise IOError, "short read on game data"

        # Search for game data magic
        found_magic = 0
        for offset in range(0, GAME_DATA_BLOCK_SIZE, GAME_DATA_SIZE):
            if self.data[offset:offset+8] == "GBMDGSBB":
                found_magic = 1

        if not found_magic:
            raise ValueError, "magic not found in game data block"

    def write(self, file):
        file.write(self.data)

class Score(object):
    """
    Daigasso! Band Brothers score
    """

    def __init__(self, file=None, raise_on_invalid=True):
        if file is None:
            self.data = "\x00" * SCORE_SIZE
            self.valid = False
            self.title = None

        else:
            self.data = file.read(SCORE_SIZE)
            if len(self.data) != SCORE_SIZE:
                raise IOError, "short read on score data"

            if self.data[:8] == "BBRS_GAK":
                self.valid = True
                self.title = \
                        self.data[0x40:0x60].decode("nintendo").strip("\x00")
            else:
                if raise_on_invalid:
                    raise ValueError, "magic not found in score"
                else:
                    self.valid = False
                    self.title = None

    def write(self, file):
        file.write(self.data)

class Save(object):
    """
    Daigasso! Band Brothers save
    """

    def __init__(self, file):
        self.game_data = GameData(file)

        self.scores = []
        for n in range(8):
            try:
                self.scores.append(Score(file, raise_on_invalid=False))
            except IOError, e:
                raise IOError, "%s (%d)" % (e, n)
            except ValueError, e:
                raise ValueError, "%s (%d)" % (e, n)

        self._padding = file.read(PADDING_SIZE)
        if len(self._padding) != PADDING_SIZE:
            raise IOError, "short read on padding"

    def write(self, file):
        self.game_data.write(file)

        for n in range(8):
            self.scores[n].write(file)

        file.write(self._padding)

# ex:et:sw=4:ts=4
