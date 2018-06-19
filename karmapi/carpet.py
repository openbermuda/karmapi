"""
Do things with magic carpets

For now, synchronise a set of carpets in one widdget
"""

from karmapi import pigfarm

class MagicMosaic(pigfarm.Space):

    def __init__(self, parent, carpets=[]):

        super().__init__(parent)

        self.carpets = carpets


    def add(self, carpet):

        self.carpets.append(carpet)
