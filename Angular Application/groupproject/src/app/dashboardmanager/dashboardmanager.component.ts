import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {getAuth} from "firebase/auth";

@Component({
  selector: 'app-dashboardmanager',
  standalone: true,
  imports: [
    NavbarComponent
  ],
  templateUrl: './dashboardmanager.component.html',
  styleUrl: './dashboardmanager.component.css'
})
export class DashboardmanagerComponent implements OnInit{

  ngOnInit() {

  }

}
