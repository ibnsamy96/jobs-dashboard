import { Injectable } from '@angular/core';
import { Observable, pipe } from 'rxjs';
import { map, tap } from 'rxjs/operators';

import { Job } from '../shared/types/job.interface';
import { JobsResponse } from '../shared/types/jobs-response.interface';
import { HttpService } from './http.service';
import { Endpoint } from '../shared/types/general-types.interface';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class JobRetrievalService {
  url = 'https://ky3irq.deta.dev';

  constructor(private httpService: HttpService) {}

  getJobs(endpoint: Endpoint, query: string): Observable<Job[]> {
    return this.httpService.get(`${this.url}/${endpoint}?query=${query}`).pipe(
      tap(console.log),

      map((response) => {
        const { results: jobsList } = response as JobsResponse;
        return jobsList;
      })
    );
  }
}
