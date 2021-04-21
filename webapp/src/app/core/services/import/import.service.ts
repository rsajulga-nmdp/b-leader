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
import { BehaviorSubject } from 'rxjs';

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
  importing : BehaviorSubject<boolean>;
  limit : number = 100;
  removedChars : string[] = ['"', '='];

  constructor(private subjectsService: SubjectsService) {
    this.importing = new BehaviorSubject(false);
  }

  formatSubjects(rows : Row[], patient : Subject[], donors : Subject[]) {
    let donGenotypes = [];
    let patGenotypes = [];
    let donIDs = [];
    let patIDs = [];
    rows.forEach(function(row){
      donGenotypes.push(row['donHlaB1'] + '+' + row['donHlaB2']);
      donIDs.push(row['donID']);
      if (row['patHlaB1']){
        patGenotypes.push(row['patHlaB1'] + '+' + row['patHlaB2']);
        patIDs.push(row['patID']);
      }
    })
    this.subjectsService.addGenotypes(patGenotypes, patient);
    this.subjectsService.addGenotypes(donGenotypes, donors);
    this.subjectsService.addIDs(patIDs, patient);
    this.subjectsService.addIDs(donIDs, donors);
  }

  parseRows(lines: Array<Array<string>>) : Row[] {
    let headers = lines.shift().map(a => a.trim());
    headers = this._numberDuplicates(headers);
    this.hlaHeaders = [];
    this.idHeaders = [];
    let line : string[];

    // Header indices
    let hlaB_indices : number[] = [];
    let id_indices : number[] = [];
    for (let j = 0; j < headers.length; j++){
      if (headers[j].match(/^B \d$/)){
        hlaB_indices.push(j);
      } else if (headers[j].match(/GRID/g)){
        id_indices.push(j);
      }
    }
    if (!hlaB_indices.length){
      line = lines[0];
      for (let i = 0; i < line.length; i++){
        if (line[i].match(/B\*/g)){
          hlaB_indices.push(i);
        } else {
          id_indices.push(i);
        }
      }
      id_indices.reverse();
      hlaB_indices.reverse();
    }
    const service = this;
    let rows : Row[] = [];
    let çç
    for (let i = 1; i <= lines.length; i++){
      let row = new Row();
      line = lines[i - 1];
      for (let j = 0; j < hlaB_indices.length; j++){
        let value = this._removeChars(line[hlaB_indices[j]]);
        if (value){
          if (j >= 2) {
            row['patHlaB' + (j - 2 + 1)] = value.includes('B*') ? value : 'B*' + value;
          } else {
            row['donHlaB' + (j + 1)] = value.includes('B*') ? value : 'B*' + value;
          }
        }
      }
      for (let k = 0; k < 2; k++){
        let prefix = k ? 'pat' : 'don';
        let idIndex = id_indices.length >= 2 ? id_indices[k] : id_indices[0];
        // if (!idIndex){
        //   idIndex = id_indices[k;]
        // }
        console.log(prefix, idIndex, id_indices, k, line);
        row[prefix + 'ID'] = this._removeChars(line[idIndex]);
      }
      rows.push(row)
    }

    // let rows = rawSubjects.map(function(rawSubject : Object) {
    //   let row = new Row();
    //   row['donHlaB1'] = rawSubject[service.hlaHeaders[1]];
    //   row['donHlaB2'] = rawSubject[service.hlaHeaders[0]];
    //   if (service.hlaHeaders.length == 4) {
    //     row['patHlaB1'] = rawSubject[service.hlaHeaders[3]];
    //     row['patHlaB2'] = rawSubject[service.hlaHeaders[2]];
    //   } else {
    //     // TODO: Process incorrect # of hla columns
    //   }
    //   for (let i = 0; i < service.hlaHeaders.length / 2; i++){
    //     let prefix = i ? 'pat' : 'don';
    //     let idHeaders = service.idHeaders.length == 2 ? service.idHeaders[i] : service.idHeaders[0];
    //     row[prefix + 'ID'] = rawSubject[idHeaders];
    //   }
    //   return row;
    // })
    return rows;
  }

  // _determineHeaders(lines: Array<Array<string>>) {
  //   let headers = lines.shift().map(a => a.trim());
  //   headers = this._numberDuplicates(headers);
  //   console.log(headers);
  //   this.hlaHeaders = [];
  //   this.idHeaders = [];
  //   for (const [key, value] of Object.entries(subject)) {
  //     if (key.match(/^B$/g) || key.match(/B\*/g)){
  //       this.hlaHeaders.push(key);
  //     } else {
  //       this.idHeaders.push(key);
  //     }
  //   }
  //   console.log(this.hlaHeaders);
  //   console.log(this.idHeaders);
  //   this.hlaHeaders.reverse();
  //   this.idHeaders.reverse();
  // }

  _numberDuplicates(headers: string[]){
    let map = {};
    const count = headers.map(function(val) {
        return map[val] = (typeof map[val] === "undefined") ? 1 : map[val] + 1;
    });
    const numberedHeaders = headers.map(function(val, index) {
        return val + (map[val] != 1 ? ' ' + count[index] : '');
    });
    return numberedHeaders;
  }

  _removeChars(value : string){
    while (value && this.removedChars.some(c => value.indexOf(c) > 0)){
      this.removedChars.forEach(c => {
        value = value.replace(c, '');
      })
    }
    return value ? value.replace(/(\r\n|\n|\r)/gm,"") : value;
  }

  setAsImporting(importing: boolean){
    this.importing.next(importing);
  }

  getLimit(){
    return this.limit;
  }
}