/*
 * Copyright (c) 2021 Be The Match.
 *
 * This file is part of BLEAT 
 * (see https://github.com/nmdp-bioinformatics/b-leader).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */
import { Injectable } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../../../../environments/environment";
import { NONE_TYPE } from '@angular/compiler/src/output/output_ast';

@Injectable({
  providedIn: 'root'
})
export class LeaderMatchingService {
  private baseURL = environment.apiUrl + '/b-leader-match/status';

  constructor(private httpClient: HttpClient) { }

  getLeaderMatchInfo(patient: Subject, donors: Subject[]): Promise<any> {
    return this.httpClient.post(this.baseURL, this._formatInput(patient, donors))
      .toPromise()
      .then((res: Object[]) => {
        return res.map((subjectInfo) => {
          // console.log(subjectInfo)
          let results = {'id' : subjectInfo['hlaB_genotype_donor']['id'],
                  'leaderMatch' : subjectInfo['leader_match_status'] ?
                                    subjectInfo['leader_match_status'].split('') :
                                    [' ',' ',' '],
                  'hlaBMatch' : subjectInfo['hlaB_genotype_match'] ?
                                  subjectInfo['hlaB_genotype_match'].split('') :
                                  ['NA','NA','NA'],
                  'leaderPatient' : subjectInfo['leader_genotype_patient'],
                  'leaderDonor' : subjectInfo['leader_genotype_donor'],
                  'leaderGenotypePatient' : subjectInfo['leader_genotype_patient']['leader_genotype'],  
                  'leaderGenotypeDonor' : subjectInfo['leader_genotype_donor']['leader_genotype'],  
                  'sharedAllotypePatient' : subjectInfo['shared_allotype_patient'],
                  'sharedAllotypeDonor' : subjectInfo['shared_allotype_donor'],
                  'flippedPatient' : subjectInfo['hlaB_genotype_patient'].flip_matched != subjectInfo['hlaB_genotype_patient'].flip_sorted,
                  'flippedDonor' : subjectInfo['hlaB_genotype_donor'].flip_matched != subjectInfo['hlaB_genotype_donor'].flip_sorted,
                  'rank' : subjectInfo['rank'],
                  'annotated' : true};
            if (results['flippedDonor']){
              results['hlaBMatch'].reverse()
            }
          return results;
        });
      })
  }

  assignLeaders(subject: Subject, subjectInfo: Object, label : string) {
    const indices = ['one', 'two'];
    const leaderInfo = subjectInfo['leader' + label];
    const sharedAllotype = subjectInfo['sharedAllotype' + label];
    const sharedAllotypePatient = label == 'Donor' ? subjectInfo['sharedAllotypePatient'] : null;
    indices.forEach(index => {
      const allotype_res = leaderInfo['hla-b_allotype_' + index]
      const allele = allotype_res['hla-b_allotype']['name'];
      const allotypes_sub = subject.allotypes.filter(a => a['hlaB'] == allele.replace('B*',''));
      let assigned = false;
      allotypes_sub.forEach(allo => {
        allo.leader = allotype_res['common_leader'];
        allo.exceptions = allotype_res['exceptions'];
        allo.unknowns = allotype_res['unknowns'];
        allo.known = allotype_res['known'];
        if (allele == sharedAllotype){
          if (sharedAllotypePatient && !assigned){
            const patientGenotype = indices.map(i => subjectInfo['leaderPatient']['hla-b_genotype']['allotype_' + i].name);
            if (subjectInfo['flippedPatient']){
              patientGenotype.reverse();
            }
            allo.sharedIndex = patientGenotype.indexOf(sharedAllotypePatient);
            assigned = true;
          } else {
            allo.sharedIndex = null;
          }
        }
      })
    })
  }

  // assignSharedAllotype(patient : Subject, donor : Subject, leaderInfo : Object){
    
  // }

  assignResults(patient: Subject, donor : Subject, leaderInfo :  Object){
    this.assignLeaders(patient, leaderInfo, 'Patient');
    this.assignLeaders(donor, leaderInfo, 'Donor');
    // this.assignSharedAllotype(patient, donor, leaderInfo);
    donor['sharedAllotype'] = leaderInfo['sharedAllotypeDonor'];
    donor.rank = null;
    donor.loading = false;
  }

  private _formatInput(patient: Subject, donors: Subject[]) {
    return {"hla-b_genotype_patient" : this._formatGenotypes([patient])[0],
            "hla-b_genotype_donors"  : this._formatGenotypes(donors)};
  }

  private _formatGenotypes(subjects: Subject[]){
    return subjects.filter(sub => sub.allotypes[0].hlaB != "" &&
                                   sub.allotypes[1].hlaB != "")
                   .map(sub => {
                     return {'id' : sub.id,
                     'genotype' : sub.allotypes.map(allo => "B*" + allo.hlaB).join('+')}
    });
  }

}
