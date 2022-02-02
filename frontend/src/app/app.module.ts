import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { JobComponent } from './shared/components/job/job.component';
import { JobRetrievalComponent } from './services/job-retrieval/job-retrieval.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    JobComponent,
    JobRetrievalComponent,
  ],
  imports: [BrowserModule, AppRoutingModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
