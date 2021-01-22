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
from behave import *
from hamcrest import assert_that, is_
from bleader.match import HlaBGenotypeMatch
from bleader.hla_b import HlaBGenotype
from bleader.mapper import LeaderMapper

@given('the patient genotype is "{genotype_patient}"')
def step_impl(context, genotype_patient):
    context.genotype_patient = HlaBGenotype(genotype_patient)

@given('a list of donor genotypes')
def step_impl(context):
    donors = []
    for row in context.table:
        donors.append(HlaBGenotype(row["HLA-B Genotype"]))
    context.genotypes_donors = donors

@when('the donors are ranked')
def step_impl(context):
    mapper = LeaderMapper()
    match = HlaBGenotypeMatch(context.genotype_patient, context.genotypes_donors)
    match_status_info = mapper.get_match_status_info(match)
    context.rank_list = ",".join([str(subj["rank"]) for subj in match_status_info])

@then('the ranks are computed to be "{rank_list}", respectively')
def step_impl(context, rank_list):
    assert_that(context.rank_list, is_(rank_list))