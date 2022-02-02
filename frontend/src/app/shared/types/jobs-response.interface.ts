import { Job } from './job.interface';

export interface JobsResponse {
  count: number;
  type: string;
  results: Job[];
}
