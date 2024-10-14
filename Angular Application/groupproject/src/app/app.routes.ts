import {RouterModule, Routes} from '@angular/router';
import {RegistrationComponent} from "./registration/registration.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {LoginComponent} from "./login/login.component";


export const routes: Routes = [
  {path: '', component: LoginComponent},
  {path: 'registration', component: RegistrationComponent},
  {path: 'dashboard', component: DashboardComponent},
  {path: '**', redirectTo: '/'}
];



