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
import { Component, OnInit, Input, Output, Inject, EventEmitter } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model'
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { SubjectsService } from '@app/core/services/subjects/subjects.service';
import { ImportService } from '@app/core/services/import/import.service';
import { Row } from '@app/core/services/import/import.service';
import { Papa } from 'ngx-papaparse';

export interface DialogData {
  dataRows: Object[];
  displayedColumns : string[];
}

@Component({
  selector: 'app-import-button',
  templateUrl: './import-button.component.html',
  styleUrls: ['./import-button.component.scss']
})
export class ImportButtonComponent implements OnInit {
  @Input() patient: Subject[];
  @Input() donors: Subject[];
  dataRows: Row[];
  @Output() sortList = new EventEmitter<Object>();
  displayedColumns : string[] = ["patID", "patHlaB1", "patHlaB2", "donID", "donHlaB1", "donHlaB2"];

  constructor(public dialog: MatDialog,
              private subjectsService: SubjectsService,
              private importService: ImportService) { }

  ngOnInit() {
  }

  import() {
    const dialogRef = this.dialog.open(ImportDialogComponent, {
      data: {dataRows : this.dataRows,
             displayedColumns : this.displayedColumns}
    });

    dialogRef.afterClosed().subscribe(result => {
      this.dataRows = result;
      if (this.dataRows){
        this._setSubjects();
      }
    })
  }

  private _setSubjects() {
    this.importService.formatSubjects(this.dataRows, this.patient, this.donors);
    if (this.patient.length == 1){
      this.sortList.emit();
    }
  }

}

@Component({
  selector: 'app-import-dialog',
  templateUrl: './import-dialog.component.html',
  styleUrls: ['./import-button.component.scss']
})
export class ImportDialogComponent implements OnInit {
  file: File;

  constructor(
    public dialogRef: MatDialogRef<ImportDialogComponent>,
    private papa: Papa,
    private importService: ImportService,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { }

  ngOnInit() {
  }

  handleFileInput($event) {
    const file = $event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      this.papa.parse(reader.result.toString(), {
        skipEmptyLines : true,
        header: true,
        complete: (result) => {
          this.importService.setAsImporting(true);
          this.data.dataRows = this.importService.parseRows(result['data']);
        }
      })
    };
    reader.readAsText(file);
  }
}
