import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import { getAuth, signOut } from "firebase/auth";



@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  auth = getAuth();
  user = this.auth.currentUser;
  username = this.user?.displayName;


  logout(){
    const auth = getAuth();
    signOut(auth).then(() =>{
      window.location.replace('')
    }).catch(console.log)
  }
}
