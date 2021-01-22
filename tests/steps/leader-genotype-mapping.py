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
from bleader.mapper import LeaderMapper

@given('the HLA-B genotype as {genotype_name}')
def step_impl(context, genotype_name):
    context.genotype = HlaBGenotype(genotype_name)

@when('translated to a leader genotype')
def step_impl(context):
    mapper = LeaderMapper()
    leader_info = mapper.get_leader_genotype_info(context.genotype)
    context.leader_genotype = (str(leader_info["hla-b_allotype_one"]["common_leader"]) +
                              str(leader_info["hla-b_allotype_two"]["common_leader"]))

@then('the leader genotype is {leaders}')
def step_impl(context, leaders):
    assert_that(context.leader_genotype, is_(leaders))