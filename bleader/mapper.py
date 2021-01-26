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
from bleader.map import LeaderMap
from bleader.hla_b import HlaBAllotype, HlaBGenotype
from bleader.match import HlaBGenotypeMatch
from bleader.leader import LeaderAllotype

class LeaderMapper(object):

    def __init__(self) -> None:
        """
        Represents the HLA-B-to-leader classification dictionary. Can provide
        leader information regarding the most common leader allotype, specific
        mapped HLA-B allotypes, and any HLA-B exceptions that do not adhere to
        the common leader allotype of a family.
        """
        leader_map = LeaderMap().leader_map
        self.map = {HlaBAllotype(allotype) : LeaderAllotype(leader_map[allotype]) 
                    for allotype in leader_map if re.search('B\*\d+(\:\d+)*$', allotype)}
    
    def get_map(self):
        map_str = {str(allotype) : str(self.map[allotype]) for allotype in self.map}
        return map_str
    
    def get_match_status_info(self, genotype_match: HlaBGenotypeMatch):
        """
        Returns match status information for a genotype match.
        :param: Genotype match consisting of two genotypes
        :type: HlaBGenotypeMatch
        """
        if not isinstance(genotype_match, HlaBGenotypeMatch):
            raise InvalidInputError(genotype_match, "Did not provide an HlaBGenotypeMatch object.")
        
        results = []
        matches = genotype_match.matches
        for match in matches:
            match_order = ["A", "P", "L", "M"]
            match_code = match['match_code']
            index_shared = index_unshared = None
            if match_order.index(match_code[0]) > match_order.index(match_code[1]):
                index_unshared, index_shared = 0, 1
            elif match_order.index(match_code[0]) < match_order.index(match_code[1]):
                index_shared, index_unshared = 0, 1

            genotype_patient = self.get_leader_genotype_info(match["genotype_patient"])
            genotype_donor = self.get_leader_genotype_info(match["genotype_donor"])
            leader_genotype_patient = genotype_patient['leader_genotype']
            leader_genotype_donor = genotype_donor['leader_genotype']
            hlaB_genotype_patient = genotype_patient['hla-b_genotype']
            hlaB_genotype_donor = genotype_donor['hla-b_genotype']

            shared_leader = shared_allotype_patient = shared_allotype_donor = leader_match_status = None
            match_status = unshared_leader_patient = unshared_leader_donor = None
            if index_shared is not None and match_code[index_shared] in ['A', 'P']:
                shared_leader = (leader_genotype_patient[index_shared]  == leader_genotype_donor[index_shared] and
                                 leader_genotype_patient[index_shared] or 'X')
                shared_allotype_patient = hlaB_genotype_patient['name'].split('+')[index_shared]
                shared_allotype_donor = hlaB_genotype_donor['name'].split('+')[index_shared]
                unshared_leader_patient = leader_genotype_patient[index_unshared]
                unshared_leader_donor = leader_genotype_donor[index_unshared]
                match_status = (unshared_leader_patient == unshared_leader_donor and 
                                'matched' or 'mismatched')
                leader_match_status = (unshared_leader_patient + unshared_leader_donor +
                                shared_leader)
            results.append({'hlaB_genotype_match' : match_code,
                            'hlaB_genotype_patient' : dict(match['genotype_patient']),
                            'hlaB_genotype_donor' : dict(match['genotype_donor']),
                            'leader_genotype_patient' : genotype_patient,
                            'leader_genotype_donor' : genotype_donor,
                            'shared_allotype_patient' : shared_allotype_patient,
                            'shared_allotype_donor' : shared_allotype_donor,
                             'shared_leader' : shared_leader,
                             'unshared_leader_patient' : unshared_leader_patient,
                             'unshared_leader_donor' : unshared_leader_donor,
                             'match_status' : match_status,
                             'leader_match_status' : (match["match_code"] not in ['AA', 'MM', 'LL', 'ML']
                                                and leader_match_status or None)})
        return self._rank(results)

    def _rank(self, results: list):
        hla_order = ["AA", "PA", "LA", "MA", "PP", "LP", "MP", "LL", "ML", "MM"]
        leader_genotype_patient = results[0]["leader_genotype_patient"]["leader_genotype"]
        leader_orders = {"MT" : ["MMT", "TTM"],
                        "TM" : ["MMT", "TTM"],
                        "TT" : ["TTT", "TMT"]}
        leader_order = (leader_genotype_patient in leader_orders and
                        leader_orders[leader_genotype_patient] or [])
        leader_order += ["other"]

        ranked_results = []
        rank = 1
        for match_status in leader_order:
            for match_code in hla_order:
                category = []
                for i, result in enumerate(results):
                    if (match_code == result["hlaB_genotype_match"] and
                        (match_status == result["leader_match_status"] or
                         (match_status == "other" and result["leader_match_status"] not in leader_order))):
                            result["rank"] = rank
                            results[i]["rank"] = rank
                            category.append(result)
                if category:
                    rank += 1
                #sorted_results += category
        return results

    def get_leader_genotype_info(self, inp_genotype: HlaBGenotype):
        """
        Returns leader genotype information from a HLA-B genotype
        :param: HLA-B genotype
        :type: HlaBGenotype or str
        """
        if not isinstance(inp_genotype, HlaBGenotype):
           inp_genotype = HlaBGenotype(inp_genotype)

        allotype_one = self.get_leader_allotype_info(inp_genotype.first())
        allotype_two = self.get_leader_allotype_info(inp_genotype.second())

        return {"leader_genotype" : str(allotype_one["common_leader"]) + str(allotype_two["common_leader"]),
                "hla-b_genotype" : dict(inp_genotype),
                "hla-b_allotype_one" : allotype_one,
                "hla-b_allotype_two" : allotype_two}

    def get_leader_allotype_info(self, inp_allotype: HlaBAllotype):
        """
        Obtains the leader classification summary of potential alleles
        from a provided HlaBAllotype by matching available fields.

        :param inp_allotype: Hla-B Allotype of which to obtain leader information
        :type inp_allotype: HlaBAllotype or str
        """
        if not isinstance(inp_allotype, HlaBAllotype):
            inp_allotype = HlaBAllotype(inp_allotype)
        output_map, family_leader = self._get_map_subset(inp_allotype.alleles)
        return self._summarize_leaders(inp_allotype, output_map, family_leader)
    
    def _get_map_subset(self, inp_allotypes: [HlaBAllotype]):
        """
        Obtains the dictionary subset of HlaBAllotypes that 
        have fields that match the input HlaBAllotypes' fields.
        :return: dictionary of str, HlaBAllotype
        """
        output_map = {}
        allele_family = []
        family_leader = None
        for allotype in inp_allotypes:
            allotype_matches = False
            for hla_b in self.map:
                if hla_b.fields[0] == allotype.fields[0]:
                    allele_family.append(self.map[hla_b].name)
                    match = True
                    i = 1
                    while (match and i < len(hla_b.fields)
                            and hla_b.fields[i] and allotype.fields[i]):
                        field = allotype.fields[i]
                        if field and field != hla_b.fields[i]:
                            match = False
                        i += 1
                    if match:
                        allotype_matches = True
                        output_map[hla_b] = self.map[hla_b]
            # If allotype did not match any allotypes in the dictionary,
            # then assign an unknown leader type.
            if (not allotype_matches and
                allotype.name not in [str(hla_b) for hla_b in output_map.keys()]):
                output_map[allotype] = 'X'
            if (len(allele_family) and
                all([str(leader) == 'X' for leader in output_map.values()])):
                    family_leaders = [allele for allele in allele_family if allele != 'X']
                    family_leader = max(set(family_leaders), key=family_leaders.count)
        return output_map, family_leader

    def _summarize_leaders(self, inp_allotype, output_map, family_leader):
        """
        Summarizes the leader classifications in the provided map subset.
        Returns the most common leader type (M or T), a list of potential
        HLA-B allotypes, and a list of HLA-B exceptions to this classification.
        For example, the B*07 family is mostly of the M type,
        but B*07:65 and B*07:271 are T.

        :param output_map: A subset of HlaBAllotype and LeaderAllotype assignments
        :type output_map: dict of HlaBAllotype, LeaderAllotype
        """
        known = []
        exceptions = []
        unknowns = []
        common_leader = family_leader or 'X'
        known_leaders = [str(leader) for leader in output_map.values() if str(leader) != 'X']
        if known_leaders:
            common_leader = max(set(known_leaders), key = known_leaders.count)
        for hla_b, leader in output_map.items():
            if str(leader) not in [common_leader, 'X']:
                exceptions.append(hla_b)
            elif str(leader) == 'X':
                unknowns.append(hla_b)
            else:
                known.append(hla_b)
        return {'hla-b_allotype' : dict(inp_allotype),
                'common_leader' : common_leader,
                'known' : known and [str(allo) for allo in known] or None,
                'unknowns' : unknowns and [str(allo) for allo in unknowns] or None,
                'exceptions' : exceptions and [str(allo) for allo in exceptions] or None}

class InvalidInputError(Exception):

    def __init__(self, genotype_match, message) -> None:
        self.genotype_match = genotype_match
        self.message = message