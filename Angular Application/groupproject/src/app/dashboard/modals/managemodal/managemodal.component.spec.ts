import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManagemodalComponent } from './managemodal.component';

describe('ManagemodalComponent', () => {
  let component: ManagemodalComponent;
  let fixture: ComponentFixture<ManagemodalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ManagemodalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ManagemodalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
