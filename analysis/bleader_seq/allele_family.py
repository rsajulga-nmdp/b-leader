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
from .leaders import Leaders
from .allele_list import AlleleList

class AlleleFamily(object):
    
    def __init__(self, name):
        self.name = name
        self.leaders = {}
        self.count = 0
    
    def add_allele(self, allele : AlleleList, broad_race: str):
        leader_type = allele.leader_type
        if leader_type not in self.leaders:
            self.leaders[leader_type] = Leaders(leader_type)
        self.leaders[leader_type].add_leader(allele, broad_race)
        self.count += 1
    
    def __repr__(self):
        leaders = '\n'.join(["%s : %s" % (leader_name, leader)
                           for leader_name, leader in self.leaders.items()])
        return leaders

class Seq(Leaders):
    def __init__(self, name):
        super().__init__(name)
     