import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {getAuth} from "firebase/auth";
import {doc, Firestore, getDoc, getFirestore} from "@angular/fire/firestore";
import {UserCheckService} from "../services/user-check.service";
import {Auth} from "@angular/fire/auth";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-userpage',
  standalone: true,
  imports: [
    NavbarComponent,
    NgIf
  ],
  templateUrl: './userpage.component.html',
  styleUrl: './userpage.component.css'
})
export class UserpageComponent implements OnInit {
  isAdmin: boolean  | undefined;
  isManager: boolean | undefined;

  constructor(
    private firestore: Firestore,
    private userCheck: UserCheckService) {}

  async ngOnInit() {
    this.isAdmin  = false;
    this.isManager = false;
    const auth = getAuth();
    const user = auth.currentUser;
    const userID = user?.uid;
    if (userID != null) {
      this.isAdmin = await this.userCheck.isUserAnAdmin(userID);
      this.isManager = await this.userCheck.isUserAnManager(userID);
      console.log("Admin: ", this.isAdmin);
      console.log("Manager: ", this.isManager);
    }
    this.fetchUserData(auth, user);
  }

  async fetchUserData(auth: Auth, user: any) {
    if (user) {
      const userRef = doc(this.firestore, "users", user.uid);
      const userDoc = await getDoc(userRef);
      if (userDoc.exists()) {
        const userData = userDoc.data();
        console.log("User Role:", userData['userType']);
      } else {
        console.log("No user data found!");
      }
    } else {
      console.log("No user is signed in.");
    }
  }
}

