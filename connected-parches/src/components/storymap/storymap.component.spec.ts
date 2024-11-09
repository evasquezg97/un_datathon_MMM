import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StorymapComponent } from './storymap.component';

describe('StorymapComponent', () => {
  let component: StorymapComponent;
  let fixture: ComponentFixture<StorymapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StorymapComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StorymapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
