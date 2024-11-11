import { AfterViewInit, Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import * as L from 'leaflet';

interface Place {
  name: string;
  lat: number;
  lng: number;
  image: string;
  subItems?: Place[];
}

// Define the custom icon
const customIcon = L.icon({
  iconUrl: 'assets/marker.png',
  shadowUrl: undefined,
  iconSize: [32, 32], // Size of the icon
  iconAnchor: [16, 32], // Point of the icon which will correspond to marker's location
  popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
  shadowSize: [41, 41] // Size of the shadow
});

// Define the sublist icon
const sublistIcon = L.icon({
  iconUrl: 'assets/sub-marker.png',
  shadowUrl: undefined,
  iconSize: [24, 24], // Size of the icon
  iconAnchor: [12, 24], // Point of the icon which will correspond to marker's location
  popupAnchor: [1, -24], // Point from which the popup should open relative to the iconAnchor
  shadowSize: [24, 24] // Size of the shadow
});

@Component({
  selector: 'app-map',
  standalone: true,
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit, OnChanges {
  private map: L.Map | undefined;
  private markers: L.Marker[] = [];
  private polylines: L.Polyline[] = [];
  @Input() coordinates: Place[] = [];
  @Input() subCoordinates: Place[] = [];
  @Output() markerClick = new EventEmitter<Place>();

  ngAfterViewInit(): void {
    this.initMap();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['coordinates'] && this.map) {
      console.log('Coordinates changed:', this.coordinates);
      this.clearMarkersAndLines();
      this.addMarkers();
      this.centerMapOnCoordinates();
    }
    if (changes['subCoordinates'] && this.map) {
      console.log('SubCoordinates changed:', this.subCoordinates);
      this.addSubMarkers();
    }
  }

  private initMap(): void {
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
      this.map = L.map(mapContainer, { zoomControl: false }).setView([6.2476, -75.5658], 13);

      L.control.zoom({
        position: 'bottomright' // Position it to your preferred location
      }).addTo(this.map);

      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
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
      marker.on('click', () => this.markerClick.emit(coord));
      this.markers.push(marker);
    });
  }

  private addSubMarkers(): void {
    if (!this.map) {
      console.error('Map is not initialized');
      return;
    }

    console.log('Adding sub markers:', this.subCoordinates);
    this.clearSubMarkersAndLines();
    this.subCoordinates.forEach(subCoord => {
      const marker = L.marker([subCoord.lat, subCoord.lng], { icon: sublistIcon }).addTo(this.map!);
      marker.bindPopup(`<b>${subCoord.name}</b><br><img src="${subCoord.image}" alt="${subCoord.name}" width="50" height="50">`);
      this.markers.push(marker);

      // Find the parent coordinate
      const parentCoord = this.coordinates.find(coord => {
        return Math.abs(coord.lat - subCoord.lat) < 0.01 && Math.abs(coord.lng - subCoord.lng) < 0.01;
      });

      if (parentCoord) {
        // Draw a line connecting the sub marker to the parent marker
        const polyline = L.polyline([[parentCoord.lat, parentCoord.lng], [subCoord.lat, subCoord.lng]], { color: 'blue' }).addTo(this.map!);
        this.polylines.push(polyline);
      }
    });
  }

  private centerMapOnCoordinates(): void {
    if (this.coordinates.length > 0) {
      const firstCoord = this.coordinates[0];
      this.map!.setView([firstCoord.lat, firstCoord.lng], 13);
    }
  }

  private clearMarkersAndLines(): void {
    this.markers.forEach(marker => {
      this.map!.removeLayer(marker);
    });
    this.markers = [];
    this.clearSubMarkersAndLines();
  }

  private clearSubMarkersAndLines(): void {
    this.markers.forEach(marker => {
      if (marker.options.icon === sublistIcon) {
        this.map!.removeLayer(marker);
      }
    });
    this.polylines.forEach(polyline => {
      this.map!.removeLayer(polyline);
    });
    this.polylines = [];
  }
}
