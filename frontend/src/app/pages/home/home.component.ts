import { Component, OnInit } from '@angular/core';
import { Job } from 'src/app/shared/types/job.interface';
import { JobRetrievalService } from '../../services/job-retrieval.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  jobList!: Job[];

  constructor(private jobRetrieval: JobRetrievalService) {}

  ngOnInit(): void {
    this.jobRetrieval.getJobs('workable', 'frontend').subscribe((jobList) => {
      this.jobList = jobList;
    });
  }
}
