import { Component } from '@angular/core';
import { ArrowButtonComponent } from '../arrow-button/arrow-button.component';
import { MatTabsModule } from '@angular/material/tabs'; // Import MatTabsModule
import { CommonModule } from '@angular/common'; // Import CommonModule

@Component({
  selector: 'app-storymap',
  standalone: true,
  imports: [ArrowButtonComponent,MatTabsModule, CommonModule],
  templateUrl: './storymap.component.html',
  styleUrls: ['./storymap.component.css']
})
export class StorymapComponent {}
