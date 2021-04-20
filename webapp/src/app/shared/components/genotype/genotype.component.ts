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
import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model'
import { LeaderMatchingService } from '@app/core/services/bleader/leaderMatching/leader-matching.service';
import { getMatScrollStrategyAlreadyAttachedError } from '@angular/cdk/overlay/typings/scroll/scroll-strategy';
import { ImportService } from '@app/core/services/import/import.service';

@Component({
  selector: 'app-genotype',
  templateUrl: './genotype.component.html',
  styleUrls: ['./genotype.component.scss']
})

export class GenotypeComponent implements OnInit {
  @Input() index: number;
  @Input() patient: Subject[];
  @Input() subject: Subject;
  @Input() subjects: Subject[];
  @Input() flippedPatient: Subject;
  @Input() multiple: Boolean;
  @Input() matchParadigm: string;
  @Input() leaderMap: Object;
  @Input() movedPatientGenotype: boolean;
  @Input() selectIndex: number;
  @Output() initiatedMatching = new EventEmitter();
  errored : boolean = false;

  constructor(private leaderMatcher: LeaderMatchingService,
    private importService: ImportService) { }

  ngOnInit() {
  }

  checkBothAllotypes() {
    if (this.subject.allotypes.map(allo => allo.hlaB)
    .every(allo => allo != "")){
      if (this.subject.type == 'donor' && this.patient[0].allotypes[0].hlaB != ""){
        this.subject.loading = true;
        this._retrieveLeaderMatchingResults()
        this.initiatedMatching.emit()
      }
    }
  }
  
  private _retrieveLeaderMatchingResults() {
    let patient = this.patient.length == 1 ? this.patient[0] : this.patient[this.index];
    if (patient.allotypes[0].hlaB == ""){ return }

    const component = this;
    this.leaderMatcher.getLeaderMatchInfo(patient, [this.subject]).then(leaderMatchInfo => {
      this.importService.setAsImporting(false);
      leaderMatchInfo.forEach((subjectInfo: Object, index: number) => {
        Object.assign(this.subject, subjectInfo)
        this.leaderMatcher.assignResults(patient, this.subject, subjectInfo);
      })
    }).catch(res => {
      console.log('TODO: Handle error response');
      if (!component.errored){
        // alert(`The back-end server for leader matching is currently down. If this persists, raise an issue at https://github.com/nmdp-bioinformatics/b-leader/issues.`)
        component.errored = true;
      } 
      console.log(res);
    })
  }

}
