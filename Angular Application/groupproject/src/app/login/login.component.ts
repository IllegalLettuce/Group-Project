import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {getAuth, GoogleAuthProvider, signInWithPopup} from "firebase/auth";

@Component({
  selector: 'app-login',
  standalone: true,
    imports: [
        RouterLink
    ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  provider = new GoogleAuthProvider();
  googleLogin(){
    const auth = getAuth();
    signInWithPopup(auth, this.provider).then((result) =>{
      const user = result.user;
      window.location.replace('/dashboard')
    })
  }

}
