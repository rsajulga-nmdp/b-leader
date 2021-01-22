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
from collections import OrderedDict
import csv

class LeaderMap(object):

    def __init__(self) -> None:
        self.table_path = "data/table/leader_map.csv"
        self.leader_map = self._init_leader_map()

    def get_map(self):
        return self.leader_map

    def _init_leader_map(self):
        leader_map = {}
        with open(self.table_path, 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    allele = row['Allele']
                    leader_type = row['Leader Type']
                    if leader_type == '*':
                        leader_type = 'X'
                    elif leader_type == '-':
                        leader_type = 'M'
                    leader_map[allele.strip()] = leader_type
                except:
                    raise InvalidLeaderMapError(self.table_path, 
                            "Mapping file is not in the correct format. "
                            "Ensure there are only two comma-delimited columns (allele, leader type).")
        return leader_map

class InvalidLeaderMapError(Exception):

    def __init__(self, path, message) -> None:
        self.file_path = path
        self.message = message