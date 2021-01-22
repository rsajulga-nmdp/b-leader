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
import { Subject } from '@app/shared/models/subject/subject.model'

@Component({
  selector: 'app-undo-button',
  templateUrl: './undo-button.component.html',
  styleUrls: ['./undo-button.component.scss']
})
export class UndoButtonComponent implements OnInit {
  @Input() donors: Subject[];
  @Input() deletedSubjects: Subject[];

  constructor() { }

  ngOnInit() {
  }

  undo() { 
    let subject = this.deletedSubjects.pop();
    this[subject.type + 's'].splice(subject.index, 0, subject);
  }
}
