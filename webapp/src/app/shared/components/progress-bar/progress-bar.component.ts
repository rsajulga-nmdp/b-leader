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
import { Component, Input, OnInit } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model';

@Component({
  selector: 'app-progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.scss']
})
export class ProgressBarComponent implements OnInit {
  @Input() donors: Subject[];
  alerted : boolean = false;

  constructor() { }

  ngOnInit() {
  }

  donorsAnnotated() {
    let numDonorsAnnotated = this.donors.filter(d => d.annotated).length;
    if (numDonorsAnnotated == 50 && numDonorsAnnotated < this.donors.length
        && !this.alerted){
      alert("Press export to finish the rest of the calculations. An annotated file will download at completion.");
      this.alerted = true;
    }
    return numDonorsAnnotated;
  }

  calculateProgress(){
    return this.donorsAnnotated() / this.donors.length * 100;
  }

}
