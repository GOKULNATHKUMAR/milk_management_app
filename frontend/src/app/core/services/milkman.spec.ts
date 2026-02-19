import { TestBed } from '@angular/core/testing';

import { Milkman } from './milkman';

describe('Milkman', () => {
  let service: Milkman;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Milkman);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
