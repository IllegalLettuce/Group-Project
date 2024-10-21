import {Routes} from '@angular/router';
import {RegistrationComponent} from "./registration/registration.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {LoginComponent} from "./login/login.component";
import {HelpsupportComponent} from "./helpsupport/helpsupport.component";


export const routes: Routes = [
  {path: '', component: LoginComponent},
  {path: 'dashboard', component: DashboardComponent},
  {path: 'helpsupport', component: HelpsupportComponent},
  {path: 'registration', component: RegistrationComponent},
  {path: '**', redirectTo: ''}
];



