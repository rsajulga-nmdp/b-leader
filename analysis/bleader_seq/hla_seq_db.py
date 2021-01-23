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
from urllib.request import urlopen
import re
from .sequence import Sequence
import numpy as np
import sys
sys.path.insert(1, '../../')
from bleader.hla_b import HlaBAllotype
from Bio import pairwise2

class GeneFeatures(object):
    def __init__(self, ref_sequence : str, delimited_sequence : str):
        self.utr5 = None
        self.exons = []
        self.introns = []
        self.utr3 = None
        self.seq = Sequence(delimited_sequence, ref_sequence=ref_sequence)
        self._parse_sequence(ref_sequence, delimited_sequence)
    
    def _parse_sequence(self, ref_sequence : str, delimited_sequence : str) -> None:
        """
        Splits IMGT sequence delimited by '|' and assigns gene features based on
        this order: 5' UTR, exon 1, intron 1, exon 2, intron 2, exon 3, intron 4,
        exon 5, intron 5, exon 6, intron 6, exon 7, 3' UTR.
        """
        gene_features = delimited_sequence.split('|')
        ref_gene_features = ref_sequence.split('|')
        gene_features.reverse()
        ref_gene_features.reverse()
        self.utr5 = self._create_seq(gene_features, ref_gene_features)
        for i in range(1, 7): # exons 1 - 6
            self.exons.append(self._create_seq(gene_features, ref_gene_features))
            self.introns.append(self._create_seq(gene_features, ref_gene_features))
        self.exons.append(self._create_seq(gene_features, ref_gene_features)) # exon 7
        self.utr3 = self._create_seq(gene_features, ref_gene_features)
    
    def _create_seq(self, gene_features : list, ref_gene_features : list) -> Sequence:
        """
        Creates Sequence object from a list of gene features, 
        popping the last item in the list,
        in conjunction with a reference list.
        """
        return Sequence(gene_features.pop(), ref_sequence=ref_gene_features.pop())

class Allele(HlaBAllotype):
    def __init__(self, name):
        super().__init__(name)
        self.gene_features = None
        self.protein = None
        self.leader_type = None

    def assign_gene_features(self, ref_sequence : str, sequence : str):
        """
        Creates gene features object
        """
        self.gene_features = GeneFeatures(ref_sequence, sequence)

    def add_prot(self, sequence : str, ref_sequence : str) -> None:
        """
        Assigns protein sequence and leader type as well.
        """
        self.protein = Sequence(sequence, seq_type="aa", ref_sequence=ref_sequence)
        self.leader_type = self.protein.seq[3]

# Antigen-level
class HlaDB(object):
    def __init__(self, locus : str, version : str = 'Latest'):
        self.locus = locus
        self.alleles = {}
        self.headers = []
        self.version = version
        self._load_allele_seqs("gen")
        self._load_allele_seqs("prot")
        
    def _load_allele_seqs(self, db_type):
        """
        Loads sequences from IMGTHLA GitHub repository
        """
        url = ("https://raw.githubusercontent.com"
               "/ANHIG/IMGTHLA/%s/alignments/"
               "%s_%s.txt" % (self.version, self.locus, db_type))
        file = urlopen(url)
        headers = {}
        pos = None
        alleles = {}
        ref_allele = None
        for i, line in enumerate(file):
            decoded_line = line.decode("utf-8")
            if decoded_line[0] == '#':
                header_match = re.match("# ([a-z]+): (.+)\n", decoded_line)
                header, value = header_match.group(1,2)
                headers[header] = value
            else:
                row = decoded_line.split()
                if len(row) > 1:
                    if db_type == "gen" and not pos and re.match('\-?\d+', row[1]):
                        db_label, pos = row
                    else:
                        allele, sequence = row[0], ''.join(row[1:])
                        if 'B*' not in allele:
                            continue
                        if not ref_allele:
                            ref_allele = allele
                        if allele not in alleles:
                            alleles[allele] = ""
                        alleles[allele] += sequence
        allele_seqs = {}
        ref_sequence = alleles[ref_allele]
        for allele_name, sequence in alleles.items():
            if allele_name not in self.alleles:
                self.alleles[allele_name] = Allele(allele_name)
            if db_type == "gen":
                self.alleles[allele_name].assign_gene_features(ref_sequence, sequence)
            elif db_type == "prot":
                self.alleles[allele_name].add_prot(sequence, ref_sequence)
            allele_seqs[allele_name] = allele
        self.headers.append(headers)

    def align_allele_family(self, allele_family : str, align_seq : str, diff_limit : int = 1,
                        limits : list=None, verbose : bool = False, verbosity : int = 0) -> list:
        allele_family = allele_family.replace('HLA-', '')
        aligned_alleles = []
        for allele in self.alleles:
            if allele_family in allele:
                # display_diff(ref_seq, minor_08xx)
                try:
                    n_diffs = self.align(allele, align_seq, verbose=verbose, verbosity=verbosity, limits=limits)
                    if n_diffs != None and 0 <= n_diffs and n_diffs <= diff_limit:
                        aligned_alleles.append(allele)
                        # if verbose:
                            # print(allele, n_diffs)
                            # if verbosity >= 1:
                            #     self.align(allele, align_seq, verbose=verbose, verbosity=verbosity, limits=limits)
                except Exception as e:
                    print("Error", allele, e)
        return aligned_alleles

    def get_processed_ref_seq(self, allele : str, aligned_seq : str) -> str:
        """
        Obtains processed reference sequence of provided allele name and aligns
        it with a provided sequence.
        """
        gene_features = self.alleles[allele].gene_features
        if not gene_features:
            return None
        seq = gene_features.seq.seq.replace('.','').replace('|', '')
        ref_seq = self.truncate_to_seq(seq, aligned_seq)
        return ref_seq


    def truncate_to_seq(self, sequence : str, aligned_seq : str) -> str:
        """
        Truncates to aligned_seq.
        """
        index_1 = index_2 = -1
        length = 0
        found_seq = False
        wiggle = 0
        while not found_seq:
            for primer_len_1 in reversed(range(13)):
                for primer_len_2 in reversed(range(13)):
                    primer_1 = aligned_seq[:primer_len_1]
                    primer_2 = aligned_seq[-1 * primer_len_2:]
                    index_1 = sequence.find(primer_1)
                    index_2 = sequence.rfind(primer_2, 1) + primer_len_2
                    if primer_2 == 'CCGAGATGCAGC':
                        index_2 = index_1 + len(aligned_seq)
                    if index_1 > 0 and index_2 > 0:
                        length = index_2 - index_1
                        found_seq = abs(len(aligned_seq) - length) <= wiggle
        #                 found_seq = len(aligned_seq) == length
                        # print(length, index_1, index_2, len(aligned_seq), found_seq)
                        if found_seq:
                            break
                if found_seq:
                    break
            wiggle += 1
        return sequence[index_1:index_2]

    def align(self, allele_name : str, Y : str, 
                limits : list=None,
                verbose: bool=False, verbosity: int=0) -> int:
            """
            Returns number of differences between aligned sequences.
            """
            X = self.get_processed_ref_seq(allele_name, Y)
            if X == None:
                return None
        #     if len(X) != len(Y):
        #         print("Lengths differ : %s, %s" % (len(X), len(Y)))
        #         return
        #     else:
            if not limits:
                limits = [0, min(len(X), len(Y))]
            limit_1, limit_2 = limits
            X = X[limit_1:limit_2]
            Y = Y[limit_1:limit_2]
            if verbose and verbosity >= 1:
                # disp_X = X[36: 36 + 72 * verbosity]
                # disp_Y = Y[36: 36 + 72 * verbosity]
                print(X)
                print(Sequence(Y, ref_sequence=X).alignment)
            alignments = pairwise2.align.globalxx(X, Y)
            scores = []
            for a in alignments:
                al1, al2, score, begin, end = a
                scores.append(score)
            n_diffs = len(Y) - max(scores)
            if verbose:
                print(allele_name, "Difference(s): %s" % n_diffs)
            # if verbose and verbosity >= 100:
            #     for a in alignments:
            #         al1, al2, score, begin, end = a
            #         if score == max(scores):
            #             print(max(scores))
            #             print(a)
            return n_diffs