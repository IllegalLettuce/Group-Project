import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {RouterLink} from "@angular/router";
import {ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    NavbarComponent,
    RouterLink,
    ReactiveFormsModule
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {
  apiForm: any;

  onSubmit() {
    window.location.replace('dashboard')
  }
}
