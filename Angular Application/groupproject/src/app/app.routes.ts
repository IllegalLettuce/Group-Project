import {Routes} from '@angular/router';
import {RegistrationComponent} from "./registration/registration.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {LoginComponent} from "./login/login.component";
import {HelpsupportComponent} from "./helpsupport/helpsupport.component";
import {DashboardmanagerComponent} from "./dashboardmanager/dashboardmanager.component";
import {authGuard} from "./auth.guard";
import {PaypalComponent} from "./paypal/paypal.component";
import {UserpageComponent} from "./userpage/userpage.component";


export const routes: Routes = [
  {path: '', component: LoginComponent, canActivate:[authGuard]},
  {path: 'registration', component: RegistrationComponent},
  {path: 'dashboard', component: DashboardComponent, canActivate:[authGuard]},
  {path: 'dasboardmanager', component: DashboardmanagerComponent, canActivate:[authGuard]},
  {path: 'userpage', component: UserpageComponent, canActivate:[authGuard]},
  {path: 'helpsupport', component: HelpsupportComponent, canActivate:[authGuard]},
  {path: 'paypal', component: PaypalComponent},
  {path: '**', redirectTo: ''}
];



