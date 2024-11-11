import { Routes } from '@angular/router';
import { StorymapComponent } from '../components/storymap/storymap.component';
import { ApplicationComponent } from '../components/application/application.component';
import { AppComponent } from './app.component';
import { LandingComponent } from '../components/landing/landing.component';


export const routes: Routes = [
    { path: '', component: LandingComponent },
    { path: 'storymap', component: StorymapComponent },
    { path: 'application', component: ApplicationComponent },
];
