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
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class LeaderMapService {
  leaderMap = {};
  baseURL = environment.apiUrl;

  constructor(private httpClient: HttpClient) {

  }

  getLeaderMap() : Object {
    this._queryLeaderMap();
    return this.leaderMap;
  }

  _queryLeaderMap() {
    console.log("Query leader map");
    return this.httpClient.get(encodeURI(this.baseURL + '/b-leader-classification/map'))
              .subscribe((res)=>{
                Object.assign(this.leaderMap, res);
              });
  }

}
