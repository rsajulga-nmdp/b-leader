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
import { Component, OnInit, Input } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model';
import { LeaderMatchingService } from '@app/core/services/bleader/leaderMatching/leader-matching.service';
import * as XLSX from 'xlsx';
import { FileSaverService } from 'ngx-filesaver';

@Component({
  selector: 'app-export-button',
  templateUrl: './export-button.component.html',
  styleUrls: ['./export-button.component.scss']
})
export class ExportButtonComponent implements OnInit {
  @Input() patient: Subject[];
  @Input() donors: Subject[];
  interrupted : boolean = false;

  constructor(private leaderMatchingService: LeaderMatchingService,
    private _FileSaverService: FileSaverService) { }

  ngOnInit() {
  }

  numAnnotatedDonors() {
    return this.donors.filter(d => d.annotated).length;
  }

  export() {
    if (this.patient.length > 1 && this.donors.length > 10){
      this._getHiddenResults();
    } else {
      this._exportSheet();
    }
  }

  _getHiddenResults() {
    for (let i = 0; i < this.donors.length; i++){
      let patient = this.patient[i];
      let donor = this.donors[i];
      if (!donor.annotated){
        this.leaderMatchingService.getLeaderMatchInfo(patient, 
          [donor]).then(leaderMatchInfo => {
            leaderMatchInfo.forEach((subjectInfo: Object) => {
              Object.assign(donor, subjectInfo);
              patient['leaderGenotype'] = subjectInfo['leaderGenotypePatient'];
              donor['leaderGenotype'] = subjectInfo['leaderGenotypeDonor'];
              donor.rank = null;
              if (this.donors.filter(d => !d.annotated).length == 0){
                this._exportSheet();
              } else {
                this._getHiddenResults();
              }
            })
          }).catch(res => {
            if (!this.interrupted){
              alert("The back-end server was interrupted." +
                   " Any completed work will be exported.")
              this._exportSheet();
              this.interrupted = true;
            }
          })
        return
      }
    }
  }

  _exportSheet() {
    const ws: XLSX.WorkSheet = XLSX.utils.aoa_to_sheet(this._formatExport());
    const csvOutput : string = XLSX.utils.sheet_to_csv(ws);
    const fileName : string = 'b-leader-results-' + this._getTime() + '.csv'
    const txtBlob = new Blob([csvOutput], { type : 'csv'});
    this._FileSaverService.save(txtBlob, fileName);
  }

  private _getTime(): string {
    var today = new Date();
    return (today.getMonth() + 1) + "-" + today.getDate() +
           "-" + today.getFullYear() +
           "_" + today.getHours() + "-" + today.getMinutes();
  }

  private _formatExport(): string[][] {
    let aoa: string[][] = [['Patient_ID',
                            'Patient_HLA-B_1',
                            'Patient_HLA-B_2',
                            'Donor_ID',
                            'Donor_HLA-B_1',
                            'Donor_HLA-B_2',
                            'Patient_B_Leader_Genotype',
                            'Donor_B_Leader_Genotype',
                            'Patient_B_Leader_Unshared',
                            'Donor_B_Leader_Unshared',
                            'Shared_B_Leader',
                            'B_Leader_Match_Status',
                            'Rank'
                          ]];
    for (let i = 0; i < this.donors.length; i++){
      let index = this.patient.length > 1 ? i : 0;
      let patient = this.patient[index];
      let donor = this.donors[i];
      aoa.push([patient.id,
                'B*' + patient.allotypes[0].hlaB,
                'B*' + patient.allotypes[1].hlaB,
                this.donors[i].id,
                'B*' + donor.allotypes[0].hlaB,
                'B*' + donor.allotypes[1].hlaB,
                patient.getLeaderAllotypes(),
                donor.getLeaderAllotypes(),
                donor.leaderMatch[0],
                donor.leaderMatch[1],
                donor.leaderMatch[2],
                donor.leaderMatch[0] == donor.leaderMatch[1] ? 'matched' : 'mismatched',
                donor.rank ? donor.rank.toString() : ''
              ])
    }
    return aoa
  }
}
