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
import { Component, OnInit, Input, Output, EventEmitter, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model';
import { SubjectRowComponent } from '@app/shared/components/subject-row/subject-row.component';
import { SubjectsService } from '@app/core/services/subjects/subjects.service';

@Component({
  selector: 'app-subject-column',
  templateUrl: './subject-column.component.html',
  styleUrls: ['./subject-column.component.scss']
})
export class SubjectColumnComponent implements OnInit, AfterViewInit {
  @Input() patient: Subject[];
  @Input() donors: Subject[];
  @Input() subjects: Subject[];
  @Input() leaderMap: Object;
  @Input() flippedPatient: boolean;
  @Input() movedPatientGenotype: boolean;
  @Input() sorting: boolean;
  @Input() type: string;
  @Input() selected: number;
  @Output() notifyMovedPatientGenotype = new EventEmitter<boolean>();
  @Output() deletedSubject = new EventEmitter<Object>();
  @Output() changeRow = new EventEmitter<Object>();
  selectIndex: number = 0;
  @ViewChild(SubjectRowComponent, {static: false}) elementView: ElementRef;
  @ViewChild('content', {static : false}) contentView: ElementRef;
  constructor(private subjectsService: SubjectsService) { }

  ngOnInit() {
  }

  updateScroll(position : number) {
    if (this.contentView){
      this.contentView.nativeElement.scrollTop = position;
    }
    // this.contentView.nativeElement.scrollTop = position;
  }

  ngAfterViewInit() {
    // console.log(this.elementView);
    // this.contentHeight = this.elementView.nativeElement.offsetHeight;
  }

  addSubject() {
    this.subjectsService.addEmptySubjects(this.subjects, this.subjects[0].type, 1);
  }
  
  
  emitMovedPatientGenotype($event: boolean){
    this.notifyMovedPatientGenotype.emit($event);
  }

  removeSubject($event: number){
    this.deletedSubject.emit(this.subjectsService.removeSubject(this.subjects, $event));
  }

  onScroll(event: Event){
    const rowHeight = 81;
    const scrollPos = event.target['scrollTop'];
    const selectIndex = Math.round(scrollPos / rowHeight);
    if (this.selectIndex != selectIndex){
      this.selectIndex = selectIndex;
      this.changeRow.emit(this.selectIndex);
    }
    // if (event.target['scrollTop'] % rowHeight == 0){
    // }
  }

}