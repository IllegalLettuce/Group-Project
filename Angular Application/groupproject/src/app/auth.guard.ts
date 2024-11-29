import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { Observable } from 'rxjs';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const auth = getAuth();

  return new Observable<boolean>((observer) => {
    console.log("preauth");
    onAuthStateChanged(auth, (user) => {
      console.log("onAuthStateChanged");
      if (user) {
        observer.next(true);
      } else {
        observer.next(false);
        router.navigate(['']).then(()=> window.location.reload());
      }
    });
  });
};
