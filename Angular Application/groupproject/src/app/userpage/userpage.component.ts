import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {getAuth} from "firebase/auth";
import {doc, Firestore, getDoc, getFirestore} from "@angular/fire/firestore";

@Component({
  selector: 'app-userpage',
  standalone: true,
  imports: [
    NavbarComponent
  ],
  templateUrl: './userpage.component.html',
  styleUrl: './userpage.component.css'
})
export class UserpageComponent implements OnInit {

  constructor(private firestore: Firestore) {}

  ngOnInit(): void {
    this.fetchUserData();
  }

  async fetchUserData() {
    const auth = getAuth();
    const user = auth.currentUser;

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

