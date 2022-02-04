import { Component, OnInit, Input } from '@angular/core';
import { JobControllerState } from '../../types/general-types.interface';
import { Job } from '../../types/job.interface';

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss'],
})
export class JobComponent implements OnInit {
  @Input() job!: Job;

  constructor() {}

  ngOnInit(): void {}

  private stateCompliment = {
    hide: 'hidden',
    hidden: 'hide',
    bookmark: 'bookmarked',
    bookmarked: 'bookmark',
    copy: 'copied',
    copied: 'copy',
  };

  controlJob(state: JobControllerState): void {
    const stateCompliment = this.stateCompliment[state];

    console.log(state);
    // UI change
    // Database change
  }
}
