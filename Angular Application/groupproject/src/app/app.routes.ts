import {Routes} from '@angular/router';
import {RegistrationComponent} from "./registration/registration.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {LoginComponent} from "./login/login.component";
import {HelpsupportComponent} from "./helpsupport/helpsupport.component";
import {DashboardmanagerComponent} from "./dashboardmanager/dashboardmanager.component";
import {authGuard} from "./auth.guard";


export const routes: Routes = [
  {path: '', component: LoginComponent},
  {path: 'registration', component: RegistrationComponent},
  {path: 'dashboard', component: DashboardComponent, canActivate:[authGuard]},
  {path: 'dasboardmanager', component: DashboardmanagerComponent, canActivate:[authGuard]},
  {path: 'helpsupport', component: HelpsupportComponent, canActivate:[authGuard]},
  {path: '**', redirectTo: ''}
];



