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
import { Allotype } from '@app/shared/models/allotype/allotype.model';

@Component({
  selector: 'app-leader-match-block',
  templateUrl: './leader-match-block.component.html',
  styleUrls: ['./leader-match-block.component.scss']
})
export class LeaderMatchBlockComponent implements OnInit {
  @Input() leaderMatch: string;
  @Input() initiatedMatching: boolean;
  @Input() index: number;
  @Input() allotypes: Allotype[];

  constructor() { }

  ngOnInit() {
  }

  highlightAllotype(highlight : boolean){
    this.allotypes.forEach(a => a.highlighted = highlight);
  }

}
