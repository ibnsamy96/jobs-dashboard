import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { JobComponent } from './shared/components/job/job.component';
import { SearchFormComponent } from './pages/home/search-form/search-form.component';
import { FirstCharSmallPipe } from './shared/components/job/first-char-small.pipe';
import { JobControllerComponent } from './shared/components/job/job-controller/job-controller.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    JobComponent,
    SearchFormComponent,
    FirstCharSmallPipe,
    JobControllerComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
