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
import { Component, OnInit } from '@angular/core';
import { LeaderMapService } from '@app/core/services/bleader/leaderMap/leader-map.service';
import { Subject } from '@app/shared/models/subject/subject.model';
import { SubjectsService } from '@app/core/services/subjects/subjects.service';

@Component({
  selector: 'app-subjects',
  templateUrl: './subjects.component.html',
  styleUrls: ['./subjects.component.scss']
})
export class SubjectsComponent implements OnInit {
  patient: Subject[] = [];
  donors: Subject[] = [];
  deletedSubjects: Subject[] = [];
  selected : number = 0;
  flippedPatient: boolean = false;
  movedPatientGenotype: boolean = false;
  leaderMap = this.leaderMapService.getLeaderMap();
  sorting: boolean;
  scrollHeight : number;

  constructor(private leaderMapService: LeaderMapService,
              private subjectsService: SubjectsService) { }

  ngOnInit() {
    this.subjectsService.addEmptySubjects(this.patient, 'patient', 1);
    this.subjectsService.addEmptySubjects(this.donors, 'donor', 1);
  }

  movePatientGenotype($event: boolean){
    this.movedPatientGenotype = $event;
  }

  stashSubject($event) {
    this.deletedSubjects.push($event);
  }

  assignSelected(index: number){
    this.selected = index;
  }

  assignSorting($event: boolean){
    this.sorting = $event;
  }
}
