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
from bleader.hla_b import HlaBAllotype
from bleader.match import HlaBAllotypeMatch

@given('that the two HLA-B allotypes are {allotype_one} and {allotype_two}')
def step_impl(context, allotype_one, allotype_two):
    context.allotype_one = HlaBAllotype(allotype_one)
    context.allotype_two = HlaBAllotype(allotype_two)

@when('evaluating the match grade between the two allotypes')
def step_impl(context):
    context.match_grade = HlaBAllotypeMatch(context.allotype_one, context.allotype_two)

@then('the match grade is found to be {match_grade}')
def step_impl(context, match_grade):
    assert_that(str(context.match_grade), is_(match_grade))
