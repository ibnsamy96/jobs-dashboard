import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobControllerComponent } from './job-controller.component';

describe('JobControllerComponent', () => {
  let component: JobControllerComponent;
  let fixture: ComponentFixture<JobControllerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ JobControllerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(JobControllerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
