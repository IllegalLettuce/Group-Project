import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardmanagerComponent } from './dashboardmanager.component';

describe('DashboardmanagerComponent', () => {
  let component: DashboardmanagerComponent;
  let fixture: ComponentFixture<DashboardmanagerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardmanagerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashboardmanagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
