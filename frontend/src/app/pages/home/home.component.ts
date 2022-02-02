import { Component, OnInit } from '@angular/core';
import { JobRetrievalService } from '../../services/job-retrieval.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  constructor(private jobRetrieval: JobRetrievalService) {}

  ngOnInit(): void {
    this.jobRetrieval.getJob('workable', 'frontend');
  }
}
