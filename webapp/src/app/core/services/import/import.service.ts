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
import { SubjectsService } from '@app/core/services/subjects/subjects.service';

export class Row {
  donID : string;
  donHlaB1 : string;
  donHlaB2 : string;
  patID : string;
  patHlaB1 : string;
  patHlaB2 : string;
}

@Injectable({
  providedIn: 'root'
})
export class ImportService {
  patient: Subject[];
  donors: Subject[];
  hlaHeaders : string[];
  idHeaders : string[];

  constructor(private subjectsService: SubjectsService) { }

  formatSubjects(rows : Row[], patient : Subject[], donors : Subject[]) {
    let donGenotypes = [];
    let patGenotypes = [];
    rows.forEach(function(row){
      donGenotypes.push(row['donHlaB1'] + '+' + row['donHlaB2']);
      if (row['patHlaB1']){
        patGenotypes.push(row['patHlaB1'] + '+' + row['patHlaB2']);
      }
    })
    this.subjectsService.addGenotypes(patGenotypes, patient);
    this.subjectsService.addGenotypes(donGenotypes, donors);
  }

  parseRows(rawSubjects : Object[]) : Row[] {
    this._determineHeaders(rawSubjects[0]);
    const service = this;

    let rows = rawSubjects.map(function(rawSubject : Object) {
      let row = new Row();
      row['donHlaB1'] = rawSubject[service.hlaHeaders[1]];
      row['donHlaB2'] = rawSubject[service.hlaHeaders[0]];
      if (service.hlaHeaders.length == 4) {
        row['patHlaB1'] = rawSubject[service.hlaHeaders[3]];
        row['patHlaB2'] = rawSubject[service.hlaHeaders[2]];
      } else {
        // TODO: Process incorrect # of hla columns
      }
      for (let i = 0; i < service.hlaHeaders.length / 2; i++){
        let prefix = i ? 'pat' : 'don';
        let idHeaders = service.idHeaders.length == 2 ? service.idHeaders[i] : service.idHeaders[0];
        row[prefix + 'ID'] = rawSubject[idHeaders];
      }
      return row;
    })
    return rows;
  }

  _determineHeaders(subject : Object) {
    this.hlaHeaders = [];
    this.idHeaders = [];
    for (const [key, value] of Object.entries(subject)) {
      if (value.match(/B\*/g)){
        this.hlaHeaders.push(key);
      } else {
        this.idHeaders.push(key);
      }
    }
    this.hlaHeaders.reverse();
    this.idHeaders.reverse();
  }
}