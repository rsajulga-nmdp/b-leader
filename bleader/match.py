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
import re
from copy import deepcopy
from bleader.hla_b import HlaBAllotype, HlaBGenotype

class HlaBAllotypeMatch(object):
    
    def __init__(self, allele_one: HlaBAllotype, allele_two: HlaBAllotype) -> None:
        """
        Represents the match status between two HLA-B allotypes.

        :param allele_one: HlaBAllotype object
        :param allele_two: HlaBAllotype object
        """
        if not (isinstance(allele_one, HlaBAllotype) and isinstance(allele_two, HlaBAllotype)):
            raise InvalidMatchError(allele_one, allele_two, "Need to provide two HlaBAllotype objects")

        self.allele_one, self.allele_two = allele_one, allele_two
        self.match_grade = self._get_overall_match_grade()

    def _get_match_grade(self, a1, a2):
        if a1.fields[0] == a2.fields[0]:
            if a1.fields[1] and a2.fields[1]:
                if a1.fields[1] == a2.fields[1]:
                    return "A"
                return "L"
            return "P"
        return "M"

    def _get_overall_match_grade(self):
        """
        Evaluates the match grade between two HLA typing codes with two-field consideration.

        Returns one of the following single-letter codes:
            A - HlaBAllotype Match - matching on both fields
            P - Potential Matches - matching on first field, ambiguity on second field
            L - HlaBAllotype Mismatch - matching on first field, mismatch on second field
            M - Mismatches - mismatch on first field
        """
        a1, a2 = self.allele_one, self.allele_two
        if a1.name == a2.name and a1.resolution == 'high' and a2.resolution != 'high':
            return 'A'
        match_grades = [self._get_match_grade(potential_allele_1, potential_allele_2)
            for potential_allele_1 in a1.alleles
            for potential_allele_2 in a2.alleles]
        if len(match_grades) == 1:
            return match_grades[0]
        else:
            if 'A' in match_grades or 'P' in match_grades:
                return 'P'
            elif 'L' in match_grades:
                return 'L'
            else:
                return 'M'

    def __str__(self) -> str:
        return self.match_grade


class HlaBGenotypeMatch(object):

    def __init__(self, genotype_patient: HlaBGenotype, genotypes_donors: list) -> None:
        """
        Represents the match status between two HLA-B genotypes as a 
        two-element list of HlaBAllotypeMatches. Also, aligns the genotypes
        with the match grades. The first genotype represents the patient/recipient while
        the second genotype represents the potential donor.

        :param genotype_patient: HlaBGenotype object
        :param genotypes_donors: List of HlaBGenotype objects
        """
        if not isinstance(genotypes_donors, list):
            genotypes_donors = [genotypes_donors]
        if not (isinstance(genotype_patient, HlaBGenotype) and 
                False not in [isinstance(geno_donor, HlaBGenotype) for geno_donor in genotypes_donors]):
            genotype_patient = HlaBGenotype(str(genotype_patient))
            genotypes_donors = [HlaBGenotype(str(geno_donor)) for geno_donor in genotypes_donors]

        self.matches = self._get_matches(genotype_patient, genotypes_donors)

    def _get_matches(self, genotype_patient, genotypes_donors):
        """
        Obtains the allotype match grades for both patient and donor.
        Returns a list of aligned genotypes (higher matched allotype
        pair on the right).

        :param: genotype_patient: HlaBGenotype object
        :param: genotypes_donors: List of HlaBGenotype objects
        """
        results = []
        for genotype_donor in genotypes_donors:
            result = self._get_match(deepcopy(genotype_patient), genotype_donor)
            results.append(result)
        return results

    def _get_match(self, genotype_one, genotype_two):
        """
        Compares the allotype matches between the forward and reverse versions of the genotypes
        to get the best match grade combination, which is whatever contains the highest match grade.

        (highest) A > P > L > M (lowest)

        The match grade combination is returned with the higher grade on the second element (right-most).
        The aligned genotypes are returned as well, in accordance with the match grade combination.
        
        Returns two HLA allotype match grades:
            AA - A genotype match occurs if both allotype pairs are allele matches.
            MA - A single mismatch constitutes one allele match and one mismatch.
            MM - A double mismatch occurs when both allotype pairs are mismatches.
            PA/PP/LP/MP - A potential single/double genotype match occurs when at least one pair has a potential match.
            LA/LP/LL/ML - A single/double allele genotype mismatch occurs when at least one pair has an allele mismatch.
        """
        g1_a, g1_b = genotype_one.allotypes
        g2_a, g2_b = genotype_two.allotypes

        match_for = [HlaBAllotypeMatch(g1_a, g2_a), HlaBAllotypeMatch(g1_b, g2_b)]
        match_rev = [HlaBAllotypeMatch(g1_a, g2_b), HlaBAllotypeMatch(g1_b, g2_a)]

        order = ['A', 'P', 'L', 'M']
        rank_for = [order.index(str(match_for[0])), order.index(str(match_for[1]))]
        rank_rev = [order.index(str(match_rev[0])), order.index(str(match_rev[1]))]

        # print(genotype_one)
        # print(genotype_two)
        # print(genotype_one.flip_sorted, genotype_one.flip_matched)
        # print(genotype_two.flip_sorted, genotype_two.flip_matched)
        # print(rank_for)
        # print(rank_rev)
        # print(str(match_for[0]), str(match_for[1]))
        # print(str(match_rev[0]), str(match_rev[1]))
        
        if min(rank_for) < min(rank_rev):
            if rank_for[0] < rank_for[1]:
                match_for.reverse()
                genotype_one.flip()
                genotype_two.flip()
            match_code = str(match_for[0]) + str(match_for[1])
        elif min(rank_for) > min(rank_rev):
            # genotype_two.flip()
            if rank_rev[0] < rank_rev[1]:
                match_rev.reverse()
                genotype_one.flip()
            else:
                genotype_two.flip()
            match_code = str(match_rev[0]) + str(match_rev[1])
        else:
            match_code = str(match_for[0]) + str(match_for[1])
        return {'match_code' : match_code,
            'genotype_patient' : deepcopy(genotype_one),
            'genotype_donor' : deepcopy(genotype_two)}
