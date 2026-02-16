import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilkmanDashboard } from './milkman-dashboard';

describe('MilkmanDashboard', () => {
  let component: MilkmanDashboard;
  let fixture: ComponentFixture<MilkmanDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MilkmanDashboard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MilkmanDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
