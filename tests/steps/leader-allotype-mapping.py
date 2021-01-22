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
from bleader.mapper import LeaderMapper

@given('the HLA-B allotype as {allotype_name}')
def step_impl(context, allotype_name):
    context.allotype = HlaBAllotype(allotype_name)

@when('translated to a leader allotype')
def step_impl(context):
    mapper = LeaderMapper()
    leader_info = mapper.get_leader_allotype_info(context.allotype)

    context.leader_allotype = leader_info['common_leader']

    known = leader_info['known'] or []
    context.known = (", ".join(known[0:3])
        or "None")

    context.exceptions = (leader_info['exceptions'] and
         ", ".join([str(allotype) for allotype in leader_info['exceptions']]) or "None")
    
    context.unknowns = (leader_info['unknowns'] and
         ", ".join([str(allotype) for allotype in leader_info['unknowns'][:3]]) or "None")

@then('the leader allotype is {leader_name}')
def step_impl(context, leader_name):
    assert_that(str(context.leader_allotype), is_(leader_name))

@then('any potential allotypes are listed as {known}')
def step_impl(context, known):
    assert_that(str(context.known), is_(known))

@then('any exceptions are listed as {exceptions}')
def step_impl(context, exceptions):
    assert_that(context.exceptions, is_(exceptions))

@then('any unknowns are listed as {unknowns}')
def step_impl(context, unknowns):
    assert_that(context.unknowns, is_(unknowns))