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
import { Input, Component, OnInit } from '@angular/core';
import { Subject } from '@app/shared/models/subject/subject.model';

@Component({
  selector: 'app-patient-panel',
  templateUrl: './patient-panel.component.html',
  styleUrls: ['./patient-panel.component.scss']
})
export class PatientPanelComponent implements OnInit {
  @Input() subjects: Subject[];
  @Input() donors: Subject[];
  @Input() selected: number;
  categories : Object = {'MT' : 
                            [{leader_match_status : 'MMT',
                              leader_match : 'Leader matched'},
                            {leader_match_status : 'TTM',
                              leader_match : 'Leader matched'},
                            {leader_match_status : 'MTT',
                              leader_match : 'Leader mismatched'},
                            {leader_match_status : 'TMM',
                              leader_match : 'Leader mismatched'}],
                          'TT' :
                            [{leader_match_status : 'TTT',
                              leader_match : 'Leader matched'},
                            {leader_match_status : 'TMT',
                              leader_match : 'Leader mismatched'}],
                          'MM' :
                            [{leader_match_status : 'MMM',
                              leader_match : 'Leader matched'},
                            {leader_match_status : 'MTM',
                              leader_match : 'Leader mismatched'}]
};

  constructor() { }

  ngOnInit() {
  }

  patientLeaderGenotype() {
    return (this.subjects[0].allotypes[0].leader + this.subjects[0].allotypes[1].leader);
  }
}
