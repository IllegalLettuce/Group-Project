// https://medium.com/@0ka/angular-firebase-create-and-read-e1fa37494f30
import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {RouterOutlet} from "@angular/router";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {NgIf} from "@angular/common";
import {addDoc, collection, Firestore} from "@angular/fire/firestore";

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

  async createHelpMsg(title: string, message: string) {
    const docRef = await addDoc(collection(this.firestore, 'help_message'), {
      title: title,
      message: message
    });
  }

  submitHelp() {
    const {title, message} = this.helpForm.value;
    this.createHelpMsg(title, message)
      .then(r => window.location.replace('dashboard'));
  }
}
