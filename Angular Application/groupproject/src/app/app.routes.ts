import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {RegistrationComponent} from "./registration/registration.component";
import {NgModule} from "@angular/core";

export const routes: Routes = [
  {path: '/login', component: LoginComponent},
  {path: '/registration', component: RegistrationComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]})

export class AppRoutes {}


