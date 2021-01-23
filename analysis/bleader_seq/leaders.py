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
from .allele_list import AlleleList

class Leaders(object):
    
    def __init__(self, name):
        self.name = name
        self.broad_races = {'AFA' : 0, 'API' : 0, 'CAU' : 0, 'NAM' : 0,
                            'HIS' : 0, 'MULTI' : 0, 'UNK' : 0}
        self.count = 0
        self.alleles = []
    
    def add_leader(self, allele : AlleleList, broad_race: str):
        self.alleles.append(allele)
        race_map = {'DEC' : 'UNK', 'HAWI' : 'API'}
        if broad_race in race_map:
            broad_race = race_map[broad_race]
        if broad_race not in self.broad_races:
            self.broad_races[broad_race] = 0
        self.broad_races[broad_race] += 1
        self.count += 1
        
        
    def __repr__(self):
        total_count = sum(self.broad_races.values())
        percentages = ' '.join(["%s - %s (%.2f)" % (broad_race, counts, counts / total_count *100)
                             for broad_race, counts in self.broad_races.items() if counts])
        return percentages