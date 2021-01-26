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
from .allele_family import AlleleFamily

class Allele(AlleleFamily):
    def __init__(self, name):
        super().__init__(name)
        
    def variation(self):
        if len([leader for leader in self.leaders.values()
                if leader.name]) > 1:
            if 'M' in self.leaders and 'T' in self.leaders:
                m_count = self.leaders['M'].count
                t_count = self.leaders['T'].count
                total_count = m_count + t_count
                if None in self.leaders:
                    total_count += self.leaders[None].count
                if t_count < m_count:
                    return t_count / total_count
                else:
                    return m_count / total_count
            else:
                print("Check " + self.name + str(self.leaders.keys()))
                return None
        else:
            return None
        
    def primary_leader(self):
        # Sets the leadre with the most counts
        leaders = {}
        for name, leader in self.leaders.items():
            leaders[name] = leader.count
        return max(leaders, key=leaders.get)
            
    def __repr__(self):
        return "%s (%s)" % (self.name, self.variation())
