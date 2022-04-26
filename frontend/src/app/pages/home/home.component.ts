import { Component, OnInit } from '@angular/core';

import { Job } from 'src/app/shared/types/job.interface';
import { JobRetrievalService } from '../../services/job-retrieval.service';
import { SearchFormValues } from './search-form/search-form.interface';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  jobList: Job[] | [] = [];
  showLoading!: boolean;
  showError!: boolean;
  didSearch = false;

  constructor(private jobRetrieval: JobRetrievalService) {}

  ngOnInit(): void {}

  searchForJobs(formValues: SearchFormValues): void {
    this.showLoading = true;

    const { query, type: endpoint } = formValues;

    this.jobRetrieval.getJobs(endpoint, query).subscribe(
      (jobList) => {
        this.didSearch = true;
        this.showLoading = false;
        this.jobList = jobList;
      },
      (error) => {
        this.didSearch = true;
        this.showLoading = false;
        this.showError = true;
        console.error(error);
      }
    );
  }
}
