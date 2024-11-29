import { inject } from '@angular/core';
import {ActivatedRouteSnapshot, CanActivateFn, Router} from '@angular/router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { Observable } from 'rxjs';

export const authGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const router = inject(Router);
  const auth = getAuth();

  return new Observable<boolean>((observer) => {

    onAuthStateChanged(auth, (user) => {
      if (user) {
        console.log("Logged in")
        if (route.routeConfig?.path === ""){
          router.navigate(['dashboard']).then(() => observer.next(false));
        }else{
          observer.next(true);
        }
      } else {
        console.log("Logged out")
        if (route.routeConfig?.path === ""){
          observer.next(true);
        }else{
          router.navigate(['']).then(() => {window.location.reload();observer.next(false);
          });
        }
      }
    });
  });
};
