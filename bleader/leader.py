#
# Copyright (c) 2021 Be The Match.
#
# This file is part of BLEAT 
# (see https://github.com/nmdp-bioinformatics/b-leader).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
class LeaderAllotype(object):

    def __init__(self, leader_name: str) -> None:
        """
        Represents a leader allotype categorized from the cleaved leader peptide from
        the first exon of HLA-B. Can either be a methionine (M) or threonine (T) variant.
        Needs to be either an M or a T. Otherwise, unmapped leaders are designated as X.

        :param leader_name: Classification of the leader peptide
        :type leader_name: str
        """
        self.name = leader_name
        # if self.name not in ['M', 'T', 'X']:
        #     raise InvalidLeaderAllotypeError(leader_name, "Leader allotype is neither M, T, nor X (undefined)")
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.name

class InvalidLeaderAllotypeError(Exception):

    def __init__(self, leader_name, message) -> None:
        self.leader_name = leader_name
        self.message = message

class LeaderGenotype(object):

    def __init__(self, leader_name) -> None:
        """
        The leader genotype is a two-letter code representing a pair of leader allotypes.
        Consists of the letters M and T, thus allowing these codes: MM, TT, MT, and TM.

        :param leader_name: Classification of leader allotypes
        :type leader_name: str
        """
        self.name = leader_name

        if self.name not in ["MM", "TT", "MT", "TM"]:
            raise InvalidLeaderGenotypeError(leader_name, "Leader genotype is not MM, TT, MT, nor TM")

class InvalidLeaderGenotypeError(Exception):

    def __init__(self, leader_name, message) -> None:
        self.leader_name = leader_name
        self.message = message