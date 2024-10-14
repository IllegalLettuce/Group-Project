import { Component } from '@angular/core';
import {RouterLink, RouterLinkActive, RouterModule, RouterOutlet} from '@angular/router';
import {NavbarComponent} from "./navbar/navbar.component";
import {CommonModule} from "@angular/common";
import firebase from 'firebase/compat/app';
import {environment} from "../environments/environment.development";
import {getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

firebase.initializeApp(environment.firebase);

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
    NavbarComponent,
    CommonModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {
  title = 'groupproject';
  provider = new GoogleAuthProvider();
  googleLogin(){
    const auth = getAuth();
    signInWithPopup(auth, this.provider).then((result) =>{
      const user = result.user;
      window.location.replace('dashboard')
    })
  }
}


