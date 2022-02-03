import { Component, Input, OnInit } from '@angular/core';

type ControllerType =
  | 'copy'
  | 'copied'
  | 'hide'
  | 'hidden'
  | 'bookmark'
  | 'bookmarked';

@Component({
  selector: 'app-job-controller',
  templateUrl: './job-controller.component.html',
  styleUrls: ['./job-controller.component.scss'],
})
export class JobControllerComponent implements OnInit {
  @Input() controllerType!: ControllerType;

  constructor() {}

  ngOnInit(): void {}
}
