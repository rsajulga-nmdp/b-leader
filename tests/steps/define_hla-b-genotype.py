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
from bleader.hla_b import HlaBGenotype, InvalidHlaBGenotypeError

@given('that the genotype name is {genotype}')
def step_impl(context, genotype):
    try:
        context.genotype = HlaBGenotype(genotype)
    except InvalidHlaBGenotypeError:
        context.genotype = "invalid"

@when('evaluating the validity of the genotype name')
def step_impl(context):
    pass

@then('the sorted genotype name is found to be {sorted_genotype}')
def step_impl(context, sorted_genotype):
    assert_that(str(context.genotype), is_(sorted_genotype))

@when('retrieving the individual allotypes')
def step_impl(context):
    try:
        context.first_allotype = context.genotype.first_allotype
        context.second_allotype = context.genotype.second_allotype
    except:
        context.first_allotype = "unavailable"
        context.second_allotype = "unavailable"

@then('the allotypes are {first_allotype} and {second_allotype}')
def step_impl(context, first_allotype, second_allotype):
    assert_that(str(context.first_allotype), is_(first_allotype))
    assert_that(str(context.second_allotype), is_(second_allotype))

@given('that the sorted genotype name is "{sorted_genotype}"')
def step_impl(context, sorted_genotype):
    context.sorted_genotype = HlaBGenotype(sorted_genotype)

@when('flipped to align with another genotype during matching')
def step_impl(context):
    context.sorted_genotype.flip()
    context.flipped = "flipped" if context.sorted_genotype.flip_matched else "not flipped"

@then('the genotype is found to be "{flipped}"')
def step_impl(context, flipped):
    assert_that(context.flipped, is_(flipped))

@then('the flipped genotype name is found to be "{genotype_name}"')
def step_impl(context, genotype_name):
    assert_that(str(context.sorted_genotype), is_(genotype_name))