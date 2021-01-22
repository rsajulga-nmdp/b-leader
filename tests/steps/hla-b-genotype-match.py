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

@given('two HLA-B genotype names as {genotype_name_one} and {genotype_name_two}')
def step_impl(context, genotype_name_one, genotype_name_two):
    context.genotype_name_one = genotype_name_one
    context.genotype_name_two = genotype_name_two

@when('sorting the order of the genotypes')
def step_impl(context):
    context.genotype_one = HlaBGenotype(context.genotype_name_one)
    context.genotype_two = HlaBGenotype(context.genotype_name_two)
    context.sort_one = context.genotype_one.flip_sorted and 'sorted' or 'unsorted'
    context.sort_two = context.genotype_two.flip_sorted and 'sorted' or 'unsorted'

@when('evaluating the match grades between the two genotypes and flipping as needed')
def step_impl(context):
    genotype_match = HlaBGenotypeMatch(context.genotype_one, context.genotype_two)
    context.match_grades = genotype_match.matches[0]['match_code']
    context.genotype_one = genotype_match.matches[0]['genotype_patient']
    context.genotype_two = genotype_match.matches[0]['genotype_donor']
    context.flip_one = context.genotype_one.flip_matched and 'flipped' or 'unflipped'
    context.flip_two = context.genotype_two.flip_matched and 'flipped' or 'unflipped'

@then('the genotypes are found to be {sort_one} and {sort_two}, respectively')
def step_impl(context, sort_one, sort_two):
    assert_that(context.sort_one, is_(sort_one))
    assert_that(context.sort_two, is_(sort_two))

@then('the match grades are found to be {match_grades}')
def step_impl(context, match_grades):
    assert_that(str(context.match_grades), is_(match_grades))

@then('the matched genotypes are found to be {matched_one} and {matched_two}')
def step_impl(context, matched_one, matched_two):
    assert_that(str(context.genotype_one), is_(matched_one))
    assert_that(str(context.genotype_two), is_(matched_two))

@then('the genotypes were matched as {flip_one} and {flip_two}, respectively')
def step_impl(context, flip_one, flip_two):
    assert_that(str(context.flip_one), is_(flip_one))
    assert_that(str(context.flip_two), is_(flip_two))