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
import { Component, OnInit, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model'
import { SortButtonComponent } from '@app/shared/components/sort-button/sort-button.component';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.scss']
})
export class ControlPanelComponent implements OnInit {
  @Input() patient: Subject[];
  @Input() donors: Subject[];
  @Input() deletedSubjects: Subject[];
  @Output() sorting: EventEmitter<boolean> = new EventEmitter();

  constructor() { }
  @ViewChild(SortButtonComponent, {static:false}) private sort_button;

  ngOnInit() {
  }

  help() { }

  emitSorting($event){
    this.sorting.emit($event);
  }

  sortDonorList($event){
    this.sort_button.sort();
  }

  addDeletedSubject($event){
    this.deletedSubjects.push($event);
  }
}
