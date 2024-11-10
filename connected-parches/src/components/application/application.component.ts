import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-application',
  standalone: true,
  imports: [CommonModule, FormsModule, MatInputModule, MatButtonModule, MatListModule],
  templateUrl: './application.component.html',
  styleUrls: ['./application.component.css']
})
export class ApplicationComponent {
  inputValue: string = '';
  items: string[] = []

  addItem() {
    this.items.push(this.queryItems());
  }

  queryItems() {
    if (this.inputValue.trim()) {
      return this.inputValue
    }

    return '';
  }
}
