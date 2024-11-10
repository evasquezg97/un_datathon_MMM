import { AfterViewInit, Component } from '@angular/core';
import * as L from 'leaflet';

@Component({
  selector: 'app-map',
  standalone: true,
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {
  private map: L.Map | undefined;

  ngAfterViewInit(): void {
    this.initMap();
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
}
