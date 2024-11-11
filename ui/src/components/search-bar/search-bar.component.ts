import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';

@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [CommonModule, FormsModule, MatInputModule, MatButtonModule, MatIconModule, MatFormFieldModule],
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent {
  inputValue: string = '';
  @Output() search = new EventEmitter<{ name: string, lat: number, lng: number, image: string }[]>();

  onSearch() {
    const randomPlaces = this.getRandomPlaces();
    this.search.emit(randomPlaces);
    this.inputValue = '';
  }

  private getRandomPlaces() {
    const baseLat = 6.2476;
    const baseLng = -75.5658;
    const places = [];
    for (let i = 0; i < 5; i++) {
      const latOffset = (Math.random() - 0.5) * 0.02; // Random offset between -0.01 and 0.01
      const lngOffset = (Math.random() - 0.5) * 0.02; // Random offset between -0.01 and 0.01
      const lat = baseLat + latOffset;
      const lng = baseLng + lngOffset;
      const name = `Place ${Math.floor(Math.random() * 1000)}`; // Random place name
      const image = 'https://via.placeholder.com/150'; // Placeholder image URL
      places.push({ name, lat, lng, image });
    }
    return places;
  }
}
