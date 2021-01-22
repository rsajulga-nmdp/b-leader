#!env/bin/python
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
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from bleader.hla_b import HlaBAllotype, HlaBGenotype
from bleader.match import HlaBAllotypeMatch, HlaBGenotypeMatch
from bleader.mapper import LeaderMapper
from bleader.map import LeaderMap

app = Flask(__name__)
api = Api(app=app)
ns_type = api.namespace('b-leader-classification', description='Classify the leader types of HLA-B allotype(s) and genotype(s).')
ns_match = api.namespace('b-leader-match', description='Classify the leader match status of a HLA-B genotype against HLA-B genotype(s).')

allele_model = api.model('allele', {'allele' : fields.String(example="B*07:02:01/B*07:02:02", required=True)})

@ns_type.route('/allotype/<string:hla_allotype_input>')
class LeaderAllotype(Resource):
    def get(self, hla_allotype_input):
        """
        returns leader-peptide allotype(s) of HLA-B allele(s)log fie
        """
        try:
            hla_allotypes = [allo.strip() for allo in list(set(hla_allotype_input.split(',')))]
            results = []
            mapper = LeaderMapper()
            for hla_allotype in hla_allotypes:
                results.append(mapper.get_leader_allotype_info(hla_allotype))
            return jsonify(results)
        except Exception as e:
            return e.__dict__, 500

@ns_type.route('/allotype')
class LeaderAllotype(Resource):
    
    @api.expect(allele_model)
    def post(self):
        """
        returns leader-peptide allotype(s) of HLA-B allele(s)log fie
        """
        try:
            hla_allotype_input = request.json['allele']
            hla_allotypes = [allo.strip() for allo in list(set(hla_allotype_input.split(',')))]
            results = []
            mapper = LeaderMapper()
            for hla_allotype in hla_allotypes:
                results.append(mapper.get_leader_allotype_info(hla_allotype))
            return jsonify(results)
        except Exception as e:
            return e.__dict__, 500

@ns_type.route("/genotype/<string:hla_genotype_input>")
class LeaderGenotype(Resource):
    def get(self, hla_genotype_input):
        """
        returns leader-peptide allotype(s) of HLA-B allele(s)
        """
        try:
            hla_genotypes = [geno.strip() for geno in list(set(hla_genotype_input.split(',')))]
            results = []
            mapper = LeaderMapper()
            for hla_genotype in hla_genotypes:
                results.append(mapper.get_leader_genotype_info(hla_genotype))
            return jsonify(results)
        except Exception as e:
            return e.__dict__, 500

@ns_type.route("/map")
class LeaderMap(Resource):
    def get(self):
        """
        returns dictionary of HLA-B allotypes and corresponding leader types.
        """
        return jsonify(LeaderMapper().get_map())

@ns_match.route("/status")
class MatchStatus(Resource):
    
    model = api.model('HLA-B Genotypes Input', 
		  {'hla-b_genotype_patient': fields.String(required = True, 
					 description="HLA-B genotype of the patient", 
					 help="HLA-B genotype format: B*XX:XX+B*YY:XX"),
            'hla-b_genotype_donors': fields.String(required = True, 
					 description="HLA-B genotype of the donor", 
					 help="HLA-B genotype format: B*XX:XX+B*YY:XX")})

    @api.expect(model)
    def post(self):
        """
         returns leader match status of single HLA-B-mismatched transplants sorted via a three-letter nomenclature: (1) non-shared patient's mismatch, (2) non-shared donor's mismatch, (3) shared allotype.
        """
        try:
            patient = request.json['hla-b_genotype_patient']
            donors = request.json['hla-b_genotype_donors']
            match = HlaBGenotypeMatch(HlaBGenotype(patient['genotype'], id=patient['id']),
                                      [HlaBGenotype(donor['genotype'], id=donor['id']) for donor in donors])
            results = LeaderMapper().get_match_status_info(match)
            return jsonify(results)
        except Exception as e:
            return e.__dict__, 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response

if __name__ == '__main__':
    app.run("0.0.0.0", "5010", debug=True)