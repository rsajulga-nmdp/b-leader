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
from bleader.hla_b import HlaBGenotype
from bleader.match import HlaBGenotypeMatch
from bleader.mapper import LeaderMapper

@given('the HLA-B genotypes as {genotype_one} and {genotype_two}')
def step_impl(context, genotype_one, genotype_two):
    context.genotype_match = HlaBGenotypeMatch(genotype_one, genotype_two)

@when('the match status between them is computed')
def step_impl(context):
    mapper = LeaderMapper()
    match_status_info = mapper.get_match_status_info(context.genotype_match)[0]
    context.match_status = match_status_info["leader_match_status"] or "invalid"

@then('the match status is found to be {match_status}')
def step_impl(context, match_status):
    assert_that(context.match_status, is_(match_status))


@given("the patient's HLA-B genotype is '{genotype_patient}'")
def step_impl(context, genotype_patient):
    context.genotype_patient = HlaBGenotype(genotype_patient)

@given("the donors' HLA-B genotypes")
def step_impl(context):
    donors = []
    for row in context.table:
        donors.append(HlaBGenotype(row["HLA-B Genotype"]))
    context.genotypes_donors = donors

@when('the match statuses are evaluated')
def step_impl(context):
    mapper = LeaderMapper()
    match = HlaBGenotypeMatch(context.genotype_patient, context.genotypes_donors)
    match_status_info = mapper.get_match_status_info(match)
    context.match_statuses = ",".join([subj["leader_match_status"] for subj in match_status_info])

@then('they are found to be "{match_statuses}"')
def step_impl(context, match_statuses):
    assert_that(context.match_statuses, is_(match_statuses))