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
import requests
import json

class HlaBAllotype(object):
    
    def __init__(self, allotype_name: str) -> None:
        """
        Represents an allotype. In this context, only B-allotypes are allowed.
        Valid allotype names start with B* followed by two multi-digit integers
        separated by colons.

        :param allotype_name: Name of the allotype
        :type allotype_name: str
        """

        self.name = allotype_name
        self.is_gl, self.alleles = self._is_gl()
        if self.is_gl:
            self.fields = None
            self.resolution = 'intermediate'
        else:
            self.locus, self.fields, self.resolution, self.var_expression, self.g_group = self._get_info()
            self.alleles = self._get_potential_alleles()

    def _is_gl(self):
        """ 
        Detects if allotype_name is in a GL format
        :return: boolean and list of HlaBAllotype objects
        """
        try:
            if '/' in self.name:
                alleles = []
                prefix = None
                if self.name.count(':') == 1:
                    prefix = self.name.split(':')[0]
                pot_alleles = self.name.split('/')
                for i, allele in enumerate(pot_alleles):
                    if ':' not in allele and prefix:
                        allele = prefix + ':' + allele
                    if i != 0 and 'B*' not in allele:
                        if ':' not in allele:
                            allele = ':'.join(pot_alleles[0].split(':')[:-1]) + ':' + allele
                        else:
                            allele = 'B*' + allele
                    allotype = HlaBAllotype(allele)
                    alleles.append(allotype)
                return True, alleles
            else:
                return False, None
        except:
            return False, None

    def _get_potential_alleles(self):
        """
        Returns the potential high-resolution alleles.
        If typing is intermediate, expands the alleles via a MAC service.
        :return: list of HlaBAllotype objects
        """
        if self.resolution == 'intermediate':
            url = "https://hml.nmdp.org/mac/api/expand?typing="
            try:
                response = requests.get(url + 'HLA-' + self.name)
                data = json.loads(response.content)
                expanded_list = [result['expanded'].replace('HLA-','') for result in data]
                return [HlaBAllotype(hla_name) for hla_name in expanded_list]
            except Exception as e:
                raise e
        else:
            return [self]

    
    def _get_info(self):
        """
        Extracts the locus name, a list of fields (integers),
        and the resolution level of the allele.
        Raises error if format is invalid.

        :return: type (str), fields (list)
        """
        try:
            locus, fields = self.name.split('*')
        except:
            raise InvalidHlaBAllotypeError(self.name, "Allele needs to contain exactly one asterisk '*'.")
        
        if locus != 'B':
            raise InvalidHlaBAllotypeError(self.name, "The allele's locus is not supported. "
                                            "Please use an HLA-B allele (ex: B*07:02).")

        if not re.match('[\d]+(\:[A-Z\d]+)*[A-Z]?$', fields):
            raise InvalidHlaBAllotypeError(self.name, "The fields are incorrectly formatted. "
                                            "Please include at least one field (integers). "
                                            "Additional fields are appended with a preceding semicolon ':'. "
                                            "For example, B*07:02 is a valid format but A*07:02: is not.")
        
        g_group =  bool(re.search('\d+G$', self.name))
        var_expression = ((re.search('\d+[A-Z]$', self.name) and not g_group) and
                          fields[-1] or None)
        if var_expression: fields = fields[:-1]

        fields = fields.split(':')
        resolution = (len(fields) == 1 and 'low' or
                           (g_group or re.match('^[A-Z]+$', fields[1])) and 'intermediate' or
                           re.match('^[0-9]+$', fields[1]) and 'high'  or None)
        while len(fields) < 4:
            fields.append(None)
        if not resolution:
            raise InvalidAlleleError(self.name, "The level of typing resolution cannot be determined.")
        return locus, fields, resolution, var_expression, g_group

    def __str__(self) -> str:
        return self.name
    
    def __iter__(self):
        yield 'name', self.name

    def __repr__(self):
        return self.name

class HlaBGenotype(object):

    def __init__(self, genotype_code, id=None) -> None:
        """
        Represents a pair of HLA-B allotypes. Needs to be delimited by either a
        '+' (unphased) or '~' (phased) character. The order of the allotypes is stored
        based on a numerical sort.

        :param genotype_code:  Two allotype names delimited by either '+' or '~'
        :type genotype_code: str
        """

        self.id = id
        if '+' in genotype_code:
            self.delimiter = '+'
        elif '~' in genotype_code:
            self.delimiter = '~'
        else:
            raise InvalidHlaBGenotypeError(genotype_code,
                    "Genotype is not split by '+' or '~'")

        allotypes = genotype_code.split(self.delimiter)

        self.allotypes = []
        for allotype in allotypes:
            self.allotypes.append(HlaBAllotype(allotype))

        if len(allotypes) != 2:
            raise InvalidHlaBGenotypeError(allotypes,
                    "Genotype does not contain exactly two allotypes")
        
        self.flip_matched = False
        self.flip_sorted = False
        self._set_name_and_allotypes(self._sort(self.allotypes))
    
    def flip(self):
        allotypes = self.allotypes
        allotypes.reverse()
        # self.flip_matched = not self.flip_matched
        self.flip_matched = True
        self._set_name_and_allotypes(allotypes)

    def _set_name_and_allotypes(self, allotypes):
        self.first_allotype, self.second_allotype = self.allotypes = allotypes
        self.name = str(self.first_allotype) + self.delimiter + str(self.second_allotype)

    def _sort(self, allotypes):
        """
        Sorts the two allotypes based on a numeric sorting of the fields, with
        priority on the first (left-most) field.
        Returns the sorted list of allotypes.

        Empty fields have lower priority over populated, numeric fields.

        :param allotypes: 
        :type allotypes: List of Allotype objects
        """
        if not allotypes[0].fields or not allotypes[1].fields:
            return allotypes
        fields_a, fields_b = allotypes[0].fields, allotypes[1].fields
        i = -1
        reversed = False
        while i < len(fields_a) - 1 and i < len(fields_b) - 1 and not reversed:
            i += 1
            if re.match('\d+', str(fields_a[i])) and re.match('\d+', str(fields_b[i])):
                field_a, field_b = int(fields_a[i]), int(fields_b[i])
            else:
                field_a, field_b = str(fields_a[i]), str(fields_b[i])
            if field_a > field_b:
                reversed = True
            elif field_a < field_b:
                break
        if reversed or (not fields_a[i] and fields_b[i]):
            allotypes.reverse()
            self.flip_sorted = True
        return allotypes

    def first(self):
        return self.allotypes[0]

    def second(self):
        return self.allotypes[1]

    def __str__(self) -> str:
        return self.name
    
    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'flip_sorted', self.flip_sorted
        yield 'flip_matched', self.flip_matched
        yield 'allotype_one', dict(self.first_allotype)
        yield 'allotype_two', dict(self.second_allotype)

class InvalidHlaBAllotypeError(Exception):

    def __init__(self, allotype_name, message) -> None:
        self.allotype_name = allotype_name
        self.message = message

class InvalidHlaBGenotypeError(Exception):

    def __init__(self, genotype_code, message) -> None:
        self.genotype_code = genotype_code
        self.message = message