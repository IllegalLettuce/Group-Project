import { TestBed } from '@angular/core/testing';

import { UserCheckService } from './user-check.service';

describe('UserCheckServiceService', () => {
  let service: UserCheckService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserCheckService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
