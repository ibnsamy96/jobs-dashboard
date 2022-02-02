import { TestBed } from '@angular/core/testing';

import { JobRetrievalService } from './job-retrieval.service';

describe('JobRetrievalService', () => {
  let service: JobRetrievalService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JobRetrievalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
