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
from bleader.leader import LeaderAllotype, InvalidLeaderAllotypeError

@given('that the leader allotype name is {leader_type}')
def step_impl(context, leader_type):
    try:
        context.leaderAllotype = LeaderAllotype(leader_type)
        context.validity = "valid"
    except:
        context.validity = "invalid"

@when('evaluating the validity of the leader allotype name')
def step_impl(context):
    pass

@then('the leader allotype name is found to be {validity}')
def step_impl(context, validity):
    assert_that(context.validity, is_(validity))