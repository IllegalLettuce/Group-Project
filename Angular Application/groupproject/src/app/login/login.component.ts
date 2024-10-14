import { Component } from '@angular/core';
import {RouterLink, RouterLinkActive} from "@angular/router";
import {AppRoutes} from "../app.routes";


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    RouterLink,
    RouterLinkActive,
    AppRoutes
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

}
