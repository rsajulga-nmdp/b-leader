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
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model'
import { LeaderClassificationService } from '@app/core/services/bleader/leaderClassification/leader-classification.service';
import { Allotype } from '@app/shared/models/allotype/allotype.model';
import { ImportService } from '@app/core/services/import/import.service';

@Component({
  selector: 'app-allotype',
  templateUrl: './allotype.component.html',
  styleUrls: ['./allotype.component.scss']
})
export class AllotypeComponent implements OnInit {
  @Input() allotype: Allotype;
  @Input() leaderMap: Object;
  @Input() subject: Subject;
  @Input() selected: boolean;
  @Input() patient: Subject;
  @Input() index: number;
  @Input() movedPatientGenotype: boolean;
  @Output() allotypeUpdated = new EventEmitter();
  sharedIndex : number = null;
  leaderType: string;
  formValue: string;
  hsl: number[];
  importing: boolean = false;

  constructor(private leaderClassification: LeaderClassificationService,
              private importService : ImportService) { }

  ngOnInit() {
    this.importService.importing.subscribe(importing => {
      this.importing = importing;
    })
  }


  getSharedIndex(){
    if (this.patient &&
        this.subject["sharedAllotypeDonor"]){
      const donorAllotypes = this.subject.allotypes.map(a => a.hlaB);
      const patientAllotypes = this.patient.allotypes.map(a => a.hlaB);
      const donorSharedIndex = donorAllotypes.indexOf(this.subject["sharedAllotypeDonor"].replace('B*',''))
      const patientSharedIndex = patientAllotypes.indexOf(this.subject["sharedAllotypePatient"].replace('B*',''));
      const sharedIndex = donorSharedIndex == patientSharedIndex ? donorSharedIndex :
                        donorSharedIndex + 10;
      return sharedIndex;
    }
  }

  updateHlaBLeader($event){// this.subject.hlaBallotypes[this.index] = $event;
    this.formValue = $event;
    if (this._validInput($event)){
      this.allotype.hlaB = $event;
      if (!this.importing){
        this._classifyLeaderType($event);
      }
      this.allotype.initiatedCall = true;
      this.allotypeUpdated.emit();
    }
  }

  private _validInput(input: string) {
    return input.match(/^\d+:[\dA-Z][\dA-Z]+([:\/][\dA-Z]+)*$/)
  }

  private _classifyLeaderType(allele: string) {
    let classification = this.leaderClassification.classifyLeaderType(allele);
    if (classification){
      classification.then(leaderInfo => {
        this.allotype.submittedHlaB = allele;
        this.allotype.leader = leaderInfo['common_leader'];
        this.allotype.exceptions = leaderInfo['exceptions'];
        this.allotype.unknowns = leaderInfo['unknowns'];
        this.allotype.known = leaderInfo['known'];
        this.allotypeUpdated.emit();
      });
    }
  }

}
