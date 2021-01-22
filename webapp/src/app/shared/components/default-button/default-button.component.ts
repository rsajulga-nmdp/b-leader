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
import { Component, OnInit, Input,
         Output, EventEmitter } from '@angular/core';
import { SubjectsService } from '@app/core/services/subjects/subjects.service';
import { Subject } from '@app/shared/models/subject/subject.model';

@Component({
  selector: 'app-default-button',
  templateUrl: './default-button.component.html',
  styleUrls: ['./default-button.component.scss']
})
export class DefaultButtonComponent implements OnInit {
  @Input() patient: Subject[];
  @Input() donors: Subject[];
  @Output() deletedSubject = new EventEmitter<Object>();

  constructor(private subjectsService: SubjectsService) { }

  ngOnInit() {
  }

  loadDefaults() {
    this.subjectsService.setDefaults(this.patient, this.donors);
  }
  
}
