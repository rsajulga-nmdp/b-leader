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
import { Subject } from '@app/shared/models/subject/subject.model';
import { LeaderMatchingService } from '@app/core/services/bleader/leaderMatching/leader-matching.service';

@Component({
  selector: 'app-sort-button',
  templateUrl: './sort-button.component.html',
  styleUrls: ['./sort-button.component.scss']
})
export class SortButtonComponent implements OnInit {
  @Input() patient: Subject[];
  @Input() donors: Subject[];
  unsortedRanks: number[];
  @Output() sorting: EventEmitter<boolean> = new EventEmitter();

  constructor(private leaderMatcher: LeaderMatchingService) { }

  ngOnInit() {
  }

  sort() {
    this.sorting.emit(true)
    this.leaderMatcher.getLeaderMatchInfo(this.patient[0], this.donors).then(leaderMatchInfo => {
      leaderMatchInfo.forEach((subjectInfo: Object, index: number) => {
        Object.assign(this.donors[index], subjectInfo)
      })
      this.unsortedRanks = this.donors.map(d => d.rank);
        this.donors.sort((a,b) => a.rank && !b.rank ? -1 :
                                  !a.rank && b.rank ? 1 :
                                  a.rank < b.rank ? -1 :
                                  a.rank > b.rank ? 1 : 0);
        this.sorting.emit(false)
    }).catch(res => {
      console.log('TODO: Handle error response');
      console.log(res);
    })
  }

  unsort(){
    let index: number;
    this.unsortedRanks.forEach(targetRank => {
      index = this.donors.indexOf(this.donors.filter(d => d.rank == targetRank)[0]);
      this.donors.push(this.donors.splice(index, 1)[0]);
    });
    delete this.unsortedRanks;
  }

}
