import {Component, OnInit} from '@angular/core';
import {RouterLink} from "@angular/router";
import { getAuth, signOut } from "firebase/auth";
import {UserCheckService} from "../services/user-check.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    RouterLink,
    NgIf
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit{
  auth = getAuth();
  user = this.auth.currentUser;
  username = this.user?.displayName;
  isManager = false;
  isAdmin = false;

  constructor(
    private userCheck: UserCheckService,
  ) {}

  ngOnInit(){
    if (!this.username){
      this.username = "Userpage";
    }
    this.getUserType()
  }

  /**
   * Admin or manager
   */
  async getUserType(){
    const userID = this.user?.uid;
    if (userID != null) {
      this.isAdmin = await this.userCheck.isUserAnAdmin(userID);
      this.isManager = await this.userCheck.isUserAnManager(userID);
    }
  }

  /**
   * Sends back to login page
   */
  logout(){
    const auth = getAuth();
    signOut(auth).then(() =>{
      window.location.replace('')
    }).catch(console.log)
  }
}
