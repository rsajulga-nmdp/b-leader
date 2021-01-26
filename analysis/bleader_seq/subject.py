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
class Subject(object):
    def __init__(self, id, project, broad_race=None):
        self.id = id
        self.project = project
        self.alleles = {}
        self.broad_race = broad_race
        
    def add_allele(self, allele_index, allele):
        self.alleles[allele_index] = allele   
    
    def __repr__(self):
        return str(self.alleles)