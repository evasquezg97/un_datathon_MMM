import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { prompts } from '../../data/prompts_pre';

@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [CommonModule, FormsModule, MatExpansionModule, MatButtonModule, MatIconModule],
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent {
  @Output() search = new EventEmitter<{ name: string, lat: number, lng: number, image: string }[]>();

  prompts = prompts;
  selectedPrompt: any = null;

  onSelect(prompt: any) {
    this.selectedPrompt = prompt;
    const places = prompt.data.map((item: any) => ({
      name: item.name,
      lat: item.Latitude,
      lng: item.Longitude,
      image: 'https://via.placeholder.com/150' // Placeholder image URL
    }));
    this.search.emit(places);
  }
}
