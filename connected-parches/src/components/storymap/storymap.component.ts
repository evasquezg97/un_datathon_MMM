import { Component } from '@angular/core';
import { ArrowButtonComponent } from '../arrow-button/arrow-button.component';

@Component({
  selector: 'app-storymap',
  standalone: true,
  imports: [ArrowButtonComponent],
  templateUrl: './storymap.component.html',
  styleUrls: ['./storymap.component.css']
})
export class StorymapComponent {}
