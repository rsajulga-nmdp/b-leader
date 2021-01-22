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
import { Allotype } from '@app/shared/models/allotype/allotype.model'

export class Subject {

    allotypes : Allotype[];
    type: string;
    id: string;
    index: number;

    leaderGenotype : string = null;
    
    leaderMatch: string[] = ["","",""];
    hlaBMatch: string[] = ["", ""];
    sharedAllotype : string = null;
    flippedPatient: boolean = false;
    flippedDonor: boolean = false;
    loading: boolean = false;
    rank: number = 0;
    annotated : boolean = false;

    constructor(hlaBallotypes: string[], type: string, id : string, index: number) {
        this.allotypes = hlaBallotypes.map(allo => new Allotype(allo));
        this.type = type;
        this.id = id;
        this.index = index;
    }

    setHlaBAllotypes(hlaBallotypes: string[]){
        for (var i = 0; i < this.allotypes.length; i++){
            this.allotypes[i].hlaB = hlaBallotypes[i];
        }
    }

    getLeaderAllotypes(){
        if (this.leaderGenotype){
            return this.leaderGenotype;
        } else {
            return this.allotypes.map(function(allotype){
                return allotype.leader
            }).join('')
        }
    }
}