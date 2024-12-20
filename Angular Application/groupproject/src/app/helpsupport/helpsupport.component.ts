// https://medium.com/@0ka/angular-firebase-create-and-read-e1fa37494f30
import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {RouterOutlet} from "@angular/router";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {NgIf} from "@angular/common";
import {addDoc, collection, Firestore} from "@angular/fire/firestore";
import {getAuth} from "firebase/auth";

@Component({
  selector: 'app-helpsupport',
  standalone: true,
  imports: [
    NavbarComponent,
    RouterOutlet,
    FormsModule,
    NgIf,
    ReactiveFormsModule
  ],
  templateUrl: './helpsupport.component.html',
  styleUrl: './helpsupport.component.css'
})
export class HelpsupportComponent {
  helpForm: FormGroup;

  constructor(private builder: FormBuilder, public firestore: Firestore) {
    this.helpForm = this.builder.group({
      title: ['', Validators.required],
      message: ['', Validators.required]
    });
  }

  /**
   * Connects to firebase and places help message
   * @param title
   * @param message
   */
  async createHelpMsg(title: string, message: string) {
    const auth = getAuth();
    const docRef = await addDoc(collection(this.firestore, 'help_message'), {
      userID: auth.currentUser?.uid,
      title: title,
      message: message
    });
  }

  /**
   * Button handler from the form
   */
  submitHelp() {
    const {title, message} = this.helpForm.value;
    this.createHelpMsg(title, message)
      .then(r => window.location.replace('dashboard'));
  }
}
