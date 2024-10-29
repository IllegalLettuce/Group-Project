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

  logout(){
    const auth = getAuth();
    signOut(auth).then(() =>{
      window.location.replace('')
    }).catch(console.log)
  }

}
