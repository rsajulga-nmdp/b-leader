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
import { SubjectsService } from '@app/core/services/subjects/subjects.service';

@Component({
  selector: 'app-clear-button',
  templateUrl: './clear-button.component.html',
  styleUrls: ['./clear-button.component.scss']
})
export class ClearButtonComponent implements OnInit {
  @Input() subjects: Subject[];
  @Output() deletedSubject = new EventEmitter<Object>();
  type : string;

  constructor(private subjectsService: SubjectsService) { }

  ngOnInit() {
    this.type = this.subjects[0].type;
  }

  clearAll (){
    for (let i = this.subjects.length - 1; i >= 0; i--){
      this.deletedSubject.emit(this.subjectsService.removeSubject(this.subjects, i));
    }
    this.subjectsService.addEmptySubjects(this.subjects, this.type, 1);
  }

}
