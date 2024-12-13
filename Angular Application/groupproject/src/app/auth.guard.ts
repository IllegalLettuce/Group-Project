import { inject } from '@angular/core';
import {ActivatedRouteSnapshot, CanActivateFn, Router} from '@angular/router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { Observable } from 'rxjs';
import {doc, Firestore, getDoc} from "@angular/fire/firestore";

export const authGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const router = inject(Router);
  const firestore = inject(Firestore);
  const auth = getAuth();

  return new Observable<boolean>((observer) => {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        console.log("User is logged in");
        if (route.routeConfig?.path === '') {
          router.navigate(['dashboard']).then(() => observer.next(false));
        } else if (route.routeConfig?.path === 'dashboardmanager') {
          const userDocRef = doc(firestore, 'users', user.uid);
          const userDocSnapshot = await getDoc(userDocRef);
          if (userDocSnapshot.exists()) {
            const userType = userDocSnapshot.data()?.['userType'];
            if (userType === 'admin') {
              console.log('Admins cannot access the dashboardmanager page.');
              router.navigate(['dashboard']).then(() => observer.next(false));
            } else {
              observer.next(true);
            }
          } else {
            console.error('User document does not exist in Firestore.');
            router.navigate(['dashboard']).then(() => observer.next(false));
          }
        } else {
          observer.next(true);
        }
      } else {
        console.log("User is logged out");
        if (route.routeConfig?.path === '') {
          observer.next(true);
        } else {
          router.navigate(['']).then(() => {
            observer.next(false);
          });
        }
      }
    });
  });
};


