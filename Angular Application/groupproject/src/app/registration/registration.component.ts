// https://medium.com/@ojiofor/angular-reactive-forms-strong-password-validation-8dbcce92eb6c
// https://stackoverflow.com/questions/71765341/confirm-password-validation-in-angular
import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {RouterLink} from "@angular/router";
import {FormBuilder, FormGroup, ReactiveFormsModule, ValidatorFn, Validators} from "@angular/forms";
import {getAuth, createUserWithEmailAndPassword} from "firebase/auth";
import {NgIf} from "@angular/common";


@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    NavbarComponent,
    RouterLink,
    ReactiveFormsModule,
    NgIf
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {
  registerForm: FormGroup;
  StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;

  constructor(private builder: FormBuilder) {

    this.registerForm = this.builder.group({
      name: ['', Validators.required],
      surname: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required, Validators.pattern(this.StrongPasswordRegx)],
      confirmPassword: ['', Validators.required]
    },{
      validators: this.ConfirmedValidator('password', 'confirmPassword')
      }
    )
  }

  ConfirmedValidator(controlName: string, matchingControlName: string) {
    return (formGroup: FormGroup) => {
      const control = formGroup.controls[controlName];
      const matchingControl = formGroup.controls[matchingControlName];
      if (
        matchingControl.errors &&
        !matchingControl.errors['confirmedValidator']
      ) {
        return;
      }
      if (control.value !== matchingControl.value) {
        matchingControl.setErrors({ confirmedValidator: true });
      } else {
        matchingControl.setErrors(null);
      }
    }
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
