import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {getAuth, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword} from "firebase/auth";
import {app} from "../../../server";
import {FormBuilder, FormGroup, ReactiveFormsModule} from "@angular/forms";


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    RouterLink,
    ReactiveFormsModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  loginForm: FormGroup;

  constructor(private builder: FormBuilder) {
    this.loginForm = this.builder.group({
      email: [''],
      password: ['']
    })
  }



  provider = new GoogleAuthProvider();
  googleLogin(){
    const auth = getAuth();
    signInWithPopup(auth, this.provider).then((result) =>{
      const user = result.user;
      window.location.replace('/dashboard')
    }).catch(console.log)
  }

  emailLogin() {
      const {email, password} = this.loginForm.value;
      const auth = getAuth();
      signInWithEmailAndPassword(auth, email, password).then((result) => {
        const user = result.user;
        window.location.replace("/dashboard")
      }).catch(console.log)
    }
}
