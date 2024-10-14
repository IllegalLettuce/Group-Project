import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {RouterLink} from "@angular/router";
import {FormBuilder, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {getAuth, createUserWithEmailAndPassword} from "firebase/auth";


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
  registerForm: FormGroup;

  constructor(private builder: FormBuilder) {
    this.registerForm = this.builder.group({
      name: [''],
      surname: [''],
      email: [''],
      password: ['']
    })
  }

  registerUser() {
    const {email, password} = this.registerForm.value;
    const auth = getAuth();
    createUserWithEmailAndPassword(auth, email, password).then((result) => {
      const user = result.user;
      window.location.replace("/dashboard")
    }).catch(console.log)
  }
}
