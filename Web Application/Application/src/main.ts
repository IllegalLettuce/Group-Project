import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { initializeApp } from "firebase/app";

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));

const firebaseConfig = {
  apiKey: "AIzaSyDmc43-y_dmrFeuJv2wcn_4faGh6OdnXtY",
  authDomain: "aim-174b.firebaseapp.com",
  projectId: "aim-174b",
  storageBucket: "aim-174b.appspot.com",
  messagingSenderId: "931812336777",
  appId: "1:931812336777:web:7be0caa44c8d4b3839d258"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
