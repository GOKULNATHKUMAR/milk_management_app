import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilkmanManagement } from './milkman-management';

describe('MilkmanManagement', () => {
  let component: MilkmanManagement;
  let fixture: ComponentFixture<MilkmanManagement>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MilkmanManagement]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MilkmanManagement);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
