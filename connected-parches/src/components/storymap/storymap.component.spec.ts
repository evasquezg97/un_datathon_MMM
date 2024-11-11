import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ArrowButtonComponent } from '../arrow-button/arrow-button.component';
import { StorymapComponent } from './storymap.component';
import { MatTabsModule } from '@angular/material/tabs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';

describe('StorymapComponent', () => {
  let component: StorymapComponent;
  let fixture: ComponentFixture<StorymapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        StorymapComponent,
        ArrowButtonComponent,
        MatTabsModule,
        BrowserAnimationsModule,
        CommonModule,
        
      ]
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