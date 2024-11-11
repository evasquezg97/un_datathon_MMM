import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { SearchBarComponent } from '../search-bar/search-bar.component';
import { MapComponent } from '../map/map.component';
import { ArrowButtonComponent } from '../arrow-button/arrow-button.component';

interface Place {
  name: string;
  lat: number;
  lng: number;
  image: string;
  subItems?: Place[];
}

@Component({
  selector: 'app-application',
  standalone: true,
  imports: [CommonModule, MatListModule, SearchBarComponent, MapComponent, ArrowButtonComponent],
  templateUrl: './application.component.html',
  styleUrls: ['./application.component.css']
})
export class ApplicationComponent {
  items: Place[] = [];
  coordinates: Place[] = [];
  subCoordinates: Place[] = [];
  openItem: Place | null = null;

  onSearch(places: Place[]) {
    this.items.push(...places);
    this.coordinates = [...this.coordinates, ...places];
  }

  onItemClick(item: Place) {
    if (this.openItem === item) {
      // Close the currently open item
      this.closeItem(item);
      this.openItem = null;
    } else {
      // Close the previously open item
      if (this.openItem) {
        this.closeItem(this.openItem);
      }
      // Open the new item
      this.openItem = item;
      if (!item.subItems) {
        item.subItems = this.getRandomSubItems(item);
        this.subCoordinates = [...this.subCoordinates, ...item.subItems];
      }
    }
  }

  private closeItem(item: Place) {
    if (item.subItems) {
      // Remove subItems from subCoordinates
      this.subCoordinates = this.subCoordinates.filter(subCoord => !item.subItems!.includes(subCoord));
      // Clear subItems
      item.subItems = undefined;
    }
  }

  private getRandomSubItems(item: Place): Place[] {
    const subItems: Place[] = [];
    for (let i = 0; i < 3; i++) {
      const latOffset = (Math.random() - 0.5) * 0.01; // Random offset between -0.005 and 0.005
      const lngOffset = (Math.random() - 0.5) * 0.01; // Random offset between -0.005 and 0.005
      const lat = item.lat + latOffset;
      const lng = item.lng + lngOffset;
      const name = `SubPlace ${Math.floor(Math.random() * 1000)}`; // Random subplace name
      const image = 'https://via.placeholder.com/150'; // Placeholder image URL
      subItems.push({ name, lat, lng, image });
    }
    return subItems;
  }
}