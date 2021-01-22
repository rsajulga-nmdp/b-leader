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
from bleader.hla_b import HlaBAllotype, InvalidHlaBAllotypeError

@given('that the allotype name is {allotype_name}')
def step_impl(context, allotype_name):
    try:
        context.allotype = HlaBAllotype(allotype_name)
        context.valid_allotype = "valid"
    except InvalidHlaBAllotypeError as e:
        print(e)
        context.valid_allotype = "invalid"

@when('evaluating the validity of the allotype name')
def step_impl(context):
    pass

@when('retrieving the field values')
def step_impl(context):
    try:
        context.fields = ', '.join([f for f in context.allotype.fields if f])
    except:
        context.fields = "invalid"

@then('the allotype name is found to be {validity}')
def step_impl(context, validity: str):
    assert_that(context.valid_allotype, is_(validity))
    
@then('the field list should be {field_list}')
def step_impl(context, field_list):
    assert_that(context.fields, is_(field_list))


@when('extracting the possible high-resolution alleles')
def step_impl(context):
    alleles = context.allotype.alleles[:3]
    allele_names = [allele.name for allele in alleles]
    context.high_res_alleles = ','.join(allele_names)

@then('the first three alleles are found to be {allele_list}')
def step_impl(context, allele_list):
    assert_that(context.high_res_alleles, is_(allele_list))