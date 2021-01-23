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
class AlleleList(object):
    def __init__(self, allele_list, exon1_AAs=None, exon1_NTs=None, id=id,
                 whole_NTs=None, length=None, method=None, source=None, project=None):
        self.allele_list = allele_list
        self.exon1_AAs = exon1_AAs  
        self.exon1_NTs = exon1_NTs
        self.whole_NTs = whole_NTs
        self.allele_family = self._get_allele_family(allele_list)
        self.leader_peptide = self._get_leader_peptide()
        self.leader_type = self._get_leader_type()
        self.length = length
        self.method = method
        self.source = source
        self.id = id
        self.verified = False
        self.project = project
    
    def _get_allele_family(self, allele_list: str) -> str:
        allele_families = set()
        for allele in allele_list.split('/'):
            allele_family = allele.split('HLA-B*')[1].split(':')[0]
            allele_families.add(allele_family)
        if len(allele_families) > 1:
            print('Allele list does not have common allele_family: ' + allele_list)
            return None
        return allele_families.pop()
        
    def _get_leader_peptide(self) -> str:
        if not self.exon1_AAs or len(self.exon1_AAs) < 12:
            return None
        return self.exon1_AAs[2:11]
        
    def _get_leader_type(self) -> str:
        if not self.leader_peptide or len(self.leader_peptide) < 2:
            return None
        return self.leader_peptide[1]
        
    def __repr__(self):
        return "%s (%s)" % (self.allele_family, self.leader_type)
