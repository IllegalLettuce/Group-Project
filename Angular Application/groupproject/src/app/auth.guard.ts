import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router } from '@angular/router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { Observable } from 'rxjs';
import {  Firestore } from '@angular/fire/firestore';
import {UserCheckService} from "./services/user-check.service";


export const authGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const router = inject(Router);
  const auth = getAuth();
  const userCheck = inject(UserCheckService);

  return new Observable<boolean>((observer) => {
    onAuthStateChanged(auth, async (user) => {
      //========================== User is logged in ===================================
      if (user) {
        if (route.routeConfig?.path === '') {
          router.navigate(['dashboard']).then(() => observer.next(false));
        } else if (route.routeConfig?.path === 'dashboardmanager') {

          const isAdmin = await userCheck.isUserAnAdmin(user.uid);
          const isManager = await  userCheck.isUserAnManager(user.uid)

          if (isAdmin) {
            console.log("User is admin")
            router.navigate(['dashboard']).then(() => observer.next(false));
          }
          else if (isManager) {
            console.log("User is manager")
            observer.next(true);
          }
        }
        else {
          observer.next(true);
        }
      }
      // =================================== User is logged out ==========================================
      else {
        if (route.routeConfig?.path === '') {
          observer.next(true);
        }
        else {
          router.navigate(['']).then(() => {
            observer.next(false);
          });
        }
      }
    });
  });
};


