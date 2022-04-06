import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  constructor(private httpClient: HttpClient) {}
  get(url: string, headers?: {}): Observable<unknown> {
    return this.httpClient.get(url, { headers: headers });
  }
}
