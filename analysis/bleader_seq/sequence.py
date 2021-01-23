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
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

class Sequence(object):
    def __init__(self, sequence, allele=None, index=0,
                    seqs=[], seq_type = "nt",
                    ref_sequence=None, id=None, source=None, reduced=False):
        self.allele = allele
        self.index = index
        self.seq_type = seq_type
        self.ref_sequence = ref_sequence
        self.seq = sequence
        self.alignment = None
        self.align_sequences()
        self.peptide = None
        self.leader_peptide = None
        self.leader_type = None
        self.seqs = seqs
        self.is_empty = self._is_empty(sequence)
        self.id = id
        self.length = len(sequence)
        self.source = source
        self.reduced = reduced

    def align_sequences(self) -> None:
        """
        If hyphens ('-') are present in the object's sequence, then
        this is labeled as an alignment (sequence) and the true sequence
        is derived by aligning against the reference sequence.
        Otherwise, an alignment is performed between the sequence
        and the reference sequence.
        """
        if not self.ref_sequence:
            return
        if '-' in self.seq and self.ref_sequence:
            self.alignment = self.seq
            self.seq = ""
            for i, nt in enumerate(self.alignment):
                if nt == "-":
                    nt = self.ref_sequence[i]
                self.seq += nt
        else:
            self.alignment = ""
            for i, nt in enumerate(self.seq):
                try:
                    if i < len(self.ref_sequence) and nt == self.ref_sequence[i]:
                        nt = '-'
                    self.alignment += nt
                except:
                    return

    def assign_peptide_info(self):
        if self.seq_type == "aa":
            self.peptide = self.seq
        self.peptide = self.translate(self.seq)
        self.leader_peptide, self.leader_type = self._calculate_leader_info()
    
    def translate(self, sequence: str) -> str:
        try:
            is_empty = all([nt == '*' for nt in sequence])
            if len(sequence) == 3 and sequence[2] == '*' and not is_empty:
                possible_AAs = set([self.translate(sequence[:2] + nt) for nt in ['A', 'T', 'G', 'C']])
                if len(possible_AAs) == 1:
                    return possible_AAs.pop()
                else:
                    return '*'
            if len(sequence) <= 3:
                if is_empty:
                    return '*'
                return str(Seq(sequence, IUPAC.unambiguous_dna) \
                                    .transcribe().translate())
            else:
                return self.translate(sequence[:3]) + self.translate(sequence[3:])
        except Exception as e:
            return '*'
    
    def contains(self, other) -> bool:
        """
        Determines if this sequence contains the other sequence.
        """
        if self.reduced:
            return any([other == seq for seq in self.seqs])
        else:
            return self.seq == other.seq
        
    def _calculate_leader_info(self) -> (str, str):
        leader_peptide = self.peptide[2:11]
        return leader_peptide, leader_peptide[1]
    
    def _is_empty(self, seq):
        return len(seq.replace('*', '')) == 0
        
    def spaced_codons(self, sequence=None):
        if not sequence:
            sequence = self.seq
        spaced_seq = ""
        for i in range(len(sequence)):
            if i and i % 3 == 0:
                spaced_seq += " "
            spaced_seq += sequence[i]
        return spaced_seq
    
    def formatted(self):
        if self.ref_sequence == self:
            return self.spaced_codons()
        min_len = min(self.ref_sequence.length, self.length)
        sequence= ''.join([self.ref_sequence.seq[i] == self.seq[i] and
                         '-' or self.seq[i] 
                        for i in range(min_len)])
        return self.spaced_codons(sequence=sequence)

    def __eq__(self, other):
        return self.seq == other.seq

    def __repr__(self):
        return self.seq