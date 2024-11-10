import { AfterViewInit, Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import * as L from 'leaflet';

// Define the custom icon
const customIcon = L.icon({
  iconUrl: 'assets/marker.png',
  shadowUrl: undefined,
  iconSize: [32, 32], // Size of the icon
  iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
  popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
  shadowSize: [41, 41] // Size of the shadow
});

@Component({
  selector: 'app-map',
  standalone: true,
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit, OnChanges {
  private map: L.Map | undefined;
  @Input() coordinates: { name: string, lat: number, lng: number, image: string }[] = [];

  ngAfterViewInit(): void {
    this.initMap();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['coordinates'] && this.map) {
      console.log('Coordinates changed:', this.coordinates);
      this.addMarkers();
    }
  }

  private initMap(): void {
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
      this.map = L.map(mapContainer).setView([6.2476, -75.5658], 13);

      L.control.zoom({
        position: 'bottomright' // Position it to your preferred location
      }).addTo(this.map);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
      }).addTo(this.map);
    } else {
      console.error('Map container not found');
    }
  }

  private addMarkers(): void {
    if (!this.map) {
      console.error('Map is not initialized');
      return;
    }

    console.log('Adding markers:', this.coordinates);
    this.coordinates.forEach(coord => {
      const marker = L.marker([coord.lat, coord.lng], { icon: customIcon }).addTo(this.map!);
      marker.bindPopup(`<b>${coord.name}</b><br><img src="${coord.image}" alt="${coord.name}" width="50" height="50">`);
    });
  }
}
