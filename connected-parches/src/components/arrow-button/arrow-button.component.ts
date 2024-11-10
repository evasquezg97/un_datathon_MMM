import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-arrow-button',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './arrow-button.component.html',
  styleUrls: ['./arrow-button.component.css']
})
export class ArrowButtonComponent {
  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/']);
  }
}
