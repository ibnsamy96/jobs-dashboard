export interface SearchFormValues {
  query: string;
  type: Endpoint;
}

export type Endpoint = 'workable' | 'wuzzuf' | 'all';
