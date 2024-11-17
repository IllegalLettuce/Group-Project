import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportmodalComponent } from './reportmodal.component';

describe('ReportmodalComponent', () => {
  let component: ReportmodalComponent;
  let fixture: ComponentFixture<ReportmodalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReportmodalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ReportmodalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
