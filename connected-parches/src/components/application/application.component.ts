import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { SearchBarComponent } from '../search-bar/search-bar.component';
import { MapComponent } from '../map/map.component';
import { ArrowButtonComponent } from '../arrow-button/arrow-button.component';

@Component({
  selector: 'app-application',
  standalone: true,
  imports: [CommonModule, MatListModule, SearchBarComponent, MapComponent, ArrowButtonComponent],
  templateUrl: './application.component.html',
  styleUrls: ['./application.component.css']
})
export class ApplicationComponent {
  items: { name: string, lat: number, lng: number, image: string }[] = [];
  coordinates: { name: string, lat: number, lng: number, image: string }[] = [];

  onSearch(places: { name: string, lat: number, lng: number, image: string }[]) {
    this.items.push(...places);
    this.coordinates = [...this.coordinates, ...places];
  }
}
