import { Component, EventEmitter, OnInit, Output } from '@angular/core';

import { SearchFormValues } from './search-form.interface';
import { Endpoint } from '../../../shared/types/general-types.interface';

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss'],
})
export class SearchFormComponent implements OnInit {
  @Output() searchQueryAdded = new EventEmitter<SearchFormValues>();

  constructor() {}

  ngOnInit(): void {}

  searchWithKeyword(query: string, type: string): void {
    console.log(query);

    this.searchQueryAdded.emit({ query, type: type as unknown as Endpoint });
  }
}
