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
import { BrowserModule } from '@angular/platform-browser';
import { FileSaverModule } from 'ngx-filesaver';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule,
         FormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialogModule,
  MatInputModule } from '@angular/material';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material';
import { MatTooltipModule } from '@angular/material/tooltip';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatchingStatusComponent } from './modules/b-leader/matching-status/matching-status.component';
import { GenotypeComponent } from './shared/components/genotype/genotype.component';
import { SubjectColumnComponent } from './shared/components/subject-column/subject-column.component';
import { ControlPanelComponent } from './shared/components/control-panel/control-panel.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { AlleleAutocompleteComponent } from './shared/components/allele-autocomplete/allele-autocomplete.component';
import { AllotypeComponent } from './shared/components/allotype/allotype.component';
import { LeaderComponent } from './shared/components/leader/leader.component';
import { IntroComponent } from './modules/b-leader/intro/intro.component';
import { SubjectsComponent } from './shared/components/subjects/subjects.component';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { SortButtonComponent } from './shared/components/sort-button/sort-button.component';
import { ExportButtonComponent } from './shared/components/export-button/export-button.component';
import { ImportButtonComponent,
         ImportDialogComponent } from './shared/components/import-button/import-button.component';
import { UndoButtonComponent } from './shared/components/undo-button/undo-button.component';
import { DiagramComponent } from './modules/b-leader/diagram/diagram.component';
import { SubjectRowComponent } from './shared/components/subject-row/subject-row.component';
import { SubjectHeaderComponent } from './shared/components/subject-header/subject-header.component';
import { MatchBlockComponent } from './shared/components/match-block/match-block.component';
import { LeaderMatchBlockComponent } from './shared/components/leader-match-block/leader-match-block.component';
import { ClearButtonComponent } from './shared/components/clear-button/clear-button.component';
import { DefaultButtonComponent } from './shared/components/default-button/default-button.component';
import { HelpButtonComponent,
         HelpDialogComponent } from './shared/components/help-button/help-button.component';
import { PatientPanelComponent } from './modules/b-leader/patient-panel/patient-panel.component';
import { RiskBarComponent } from './modules/b-leader/risk-bar/risk-bar.component';
import { FootbarComponent } from './shared/components/footbar/footbar.component';
import { ProgressBarComponent } from './shared/components/progress-bar/progress-bar.component';

import { Papa } from 'ngx-papaparse';
import { FileSaverService } from 'ngx-filesaver';

@NgModule({
  declarations: [
    AppComponent,
    MatchingStatusComponent,
    GenotypeComponent,
    SubjectColumnComponent,
    ControlPanelComponent,
    AlleleAutocompleteComponent,
    AllotypeComponent,
    LeaderComponent,
    IntroComponent,
    SubjectsComponent,
    NavbarComponent,
    SortButtonComponent,
    ExportButtonComponent,
    ImportButtonComponent,
    UndoButtonComponent,
    ImportDialogComponent,
    DiagramComponent,
    SubjectRowComponent,
    SubjectHeaderComponent,
    MatchBlockComponent,
    LeaderMatchBlockComponent,
    ClearButtonComponent,
    DefaultButtonComponent,
    HelpButtonComponent,
    HelpDialogComponent,
    PatientPanelComponent,
    RiskBarComponent,
    FootbarComponent,
    ProgressBarComponent
  ],
  entryComponents: [
    ImportDialogComponent,
    HelpDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FileSaverModule,
    FormsModule,
    MatAutocompleteModule,
    MatFormFieldModule,
    MatInputModule,
    MatDialogModule,
    MatProgressBarModule,
    MatTableModule,
    MatTooltipModule,
    NgbModule,
    BrowserAnimationsModule,
    HttpClientModule
  ],
  exports: [
    MatDialogModule,
    MatProgressBarModule
  ],
  providers: [Papa, FileSaverService],
  bootstrap: [AppComponent]
})
export class AppModule { }
