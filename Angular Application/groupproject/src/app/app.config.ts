import {ApplicationConfig, Component, inject, OnInit} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { getAuth, provideAuth } from '@angular/fire/auth';
import { getAnalytics, provideAnalytics, ScreenTrackingService, UserTrackingService } from '@angular/fire/analytics';
import {collection, Firestore, getDocs, getFirestore, provideFirestore} from '@angular/fire/firestore';
import {provideHttpClient} from "@angular/common/http";

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes),
    provideClientHydration(),
    provideHttpClient(),
    provideAnimationsAsync(),
    provideFirebaseApp(() => initializeApp(
      {"projectId":"year3groupproject-ee682",
        "appId":"1:174849208599:web:758e24d65760a011b38752",
        "databaseURL":"https://year3groupproject-ee682-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket":"year3groupproject-ee682.appspot.com",
        "apiKey":"AIzaSyBuQ88U_qmLptVRm7IhpgrlPkNkla_4Li4",
        "authDomain":"year3groupproject-ee682.firebaseapp.com",
        "messagingSenderId":"174849208599",
        "measurementId":"G-517YYC8LQR"})),
    provideAuth(() => getAuth()),
    provideAnalytics(() => getAnalytics()),
    ScreenTrackingService,
    UserTrackingService,
    provideFirestore(() => getFirestore())],

};
