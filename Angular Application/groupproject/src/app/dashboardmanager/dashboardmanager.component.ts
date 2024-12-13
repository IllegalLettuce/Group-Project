import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";

@Component({
  selector: 'app-dashboardmanager',
  standalone: true,
  imports: [
    NavbarComponent
  ],
  templateUrl: './dashboardmanager.component.html',
  styleUrl: './dashboardmanager.component.css'
})
export class DashboardmanagerComponent {

}
