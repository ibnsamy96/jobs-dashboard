import { Injectable } from '@angular/core';
import { HttpService } from './http.service';

type Endpoint = 'workable' | 'wuzzuf' | 'all';

@Injectable({
  providedIn: 'root',
})
export class JobRetrievalService {
  url = 'https://ky3irq.deta.dev';

  constructor(private httpService: HttpService) {}

  getJob(endpoint: Endpoint, query: string): void {
    this.httpService.get(`${this.url}/${endpoint}?query=${query}`);
  }
}
