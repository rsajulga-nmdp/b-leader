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
from .sequence import Sequence
import re
import pandas as pd
import sys
sys.path.append('../')
from bleader.hla_b import HlaBAllotype as Allele

class HlaBMap(object):
    
    def __init__(self, filename):
        self.exon1_map = self._load_csv_map(filename)
        self.exon1_expanded = self._get_exon1_expanded()

    def get_exon1_seqs(self, allele_name : str) -> Sequence:
        allele_name = allele_name.replace(':XX', '').replace('HLA-', '')
        allele_name = re.sub('[A-Z]$', '', allele_name)
        if allele_name == 'B*47:01:01:01':
            allele_name = 'B*47:01:01:03'
        if allele_name in self.exon1_map:
            return self.exon1_map[allele_name]
        elif allele_name in self.exon1_expanded:
            return self.exon1_expanded[allele_name]
        else:
            try:
                allele = Allele(allele_name)
                seqs = [self.get_exon1_seqs(pot_allele.name)
                            for pot_allele in allele.alleles]
                return self.consensus_seq(allele_name, seqs)
            except Exception as e:
                print(e)
                raise InvalidAlleleError(allele_name, "Allele doesn't reduce.")
                
    def _find_original_seqs(self, allele : str, exon1_map : dict) -> list:
        return [seq for ref_allele, seq in exon1_map.items() 
                if self._is_lower_res_allele(allele, ref_allele)]

    def _is_lower_res_allele(self, lower_res_allele : str, allele : str):
        if self._has_var_expression(lower_res_allele):
            lower_res_allele = lower_res_allele[:-1]
        return bool(re.match('%s(:\d+)*[A-Z]?$' % lower_res_allele.replace('*', '\*'), allele))

    def _load_csv_map(self, filename : str) -> dict:
        exon1_df = pd.read_csv(filename)
        exon1_dict = exon1_df.set_index('Allele').to_dict()['Sequence']
        return {re.sub('[A-Z]$', '', allele) : Sequence(seq, allele=allele) for allele, seq in exon1_dict.items()}


    def _get_exon1_expanded(self) -> dict:
        exon1_expanded = {}
        print("Expanding exon 1 map starting with %s alleles" % len(self.exon1_map))
        for i, (allele, sequence) in enumerate(self.exon1_map.items()):
            lower_res_allele = self._backed_down_allele(allele)
            if i % round(len(self.exon1_map) / 20) == 0:
                print(i)
            while lower_res_allele:
                self._expand_exon1_map(lower_res_allele, exon1_expanded)
                lower_res_allele = self._backed_down_allele(lower_res_allele)
        return exon1_expanded

    def _has_var_expression(self, allele : str):
        return bool(re.match('.+[A-Z]$', allele))

    def _backed_down_allele(self, allele : str):
        fields = allele.split(':')
        
        if len(fields) > 1:
            return (':'.join(fields[:-1]) + 
                (self._has_var_expression(allele) and fields[-1][-1] or ''))
        return None

    def _expand_exon1_map(self, lower_res_allele : str, exon1_expanded : dict) -> None:
        if lower_res_allele not in exon1_expanded and lower_res_allele not in self.exon1_map:
            unique_seqs = [sequence for allele, sequence in self.exon1_map.items()
                            if self._is_lower_res_allele(lower_res_allele, allele)]
            if unique_seqs:
                sequence = self.consensus_seq(lower_res_allele, unique_seqs)
                exon1_expanded[lower_res_allele] = sequence

    def consensus_seq(self, allele, seqs : list):
        min_length = min([seq.length for seq in seqs])
        consensus_seq = ""
        for i in range(min_length):
            nts = set([s.seq[i] for s in seqs if s.seq[i] != '*'])
            nt = len(nts) == 1 and nts.pop() or '*'
            consensus_seq += nt
        return Sequence(consensus_seq, allele=allele, seqs=seqs, reduced=True)

class InvalidAlleleError(Exception):

    def __init__(self, allele, msg):
        self.allele = allele
        self.message = msg