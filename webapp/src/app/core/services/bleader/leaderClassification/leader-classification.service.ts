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
import { HttpClient, HttpResponse } from '@angular/common/http';
import { environment } from "../../../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class LeaderClassificationService {
  private baseURL = environment.apiUrl + '/b-leader-classification/allotype';

  constructor(private httpClient: HttpClient) { }

  classifyLeaderType(hlaB: string): Promise<Object> {
    return this.httpClient.post(this.baseURL, {"allele" : "B*" + hlaB})
    // return this.httpClient.get(encodeURI(this.baseURL + 'B*' + hlaB))
        .toPromise()
        .then(this._extractDatum)
        .catch(err => {
          return Promise.reject(err.error || 'Server error');
        });
  }

  private _extractDatum(res: HttpResponse<Object>) {
    return res[0];
  }



}
