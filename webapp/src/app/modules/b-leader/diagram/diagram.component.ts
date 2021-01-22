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
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model';

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.scss']
})
export class DiagramComponent implements OnInit, OnChanges {
  @Input() index: number;
  @Input() subject: Subject;
  hsl: number[];

  constructor() { }

  ngOnInit() {
  }

  ngOnChanges() {
    this._calculateHSL();
  }

  private _calculateHSL(){
    const fields = this.subject.allotypes[this.index].hlaB.split(':');
    this.hsl = [parseInt(fields[0]) % 300,
                100 - ((fields[1] ? parseInt(fields[1]) * 10 : 0) % 100),
                50 + ((fields[2] ? parseInt(fields[2]) : 0) % 50)];
  }
}
