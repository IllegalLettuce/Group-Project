import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {getAuth} from "firebase/auth";
import {environment} from '../../environments/environment.development';
import {HttpClient} from "@angular/common/http";
import {NgForOf} from "@angular/common";
import {Router} from "@angular/router";

@Component({
  selector: 'app-dashboardmanager',
  standalone: true,
  imports: [
    NavbarComponent,
    NgForOf
  ],
  templateUrl: './dashboardmanager.component.html',
  styleUrl: './dashboardmanager.component.css'
})
export class DashboardmanagerComponent implements OnInit{
  companies: {
    adminID: any,
    companyName: string
  }[] = [];

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit() {
    console.log("Dashboard manager component");
    const uriGetCompanies = environment.API_BASE_URL + "/getcompanies";
    const auth = getAuth();
    let managerID = auth.currentUser?.uid;

    const json_manager = {
      "managerID": managerID
    }
    this.http.post<any[]>(uriGetCompanies, json_manager).subscribe(
      (response)=>{
        this.companies = response;
        console.log(response);
      }
    )
  }

  /**
   * Goes to the dashboard for a specific admin
   * @param adminID
   */
  manageCompany(adminID: any){
    this.router.navigate(['/dashboard'], { queryParams: { adminID } });
  }

  /**
   * Goes to the userpage for a specific admin
   * @param adminID
   */
  manageAdmin(adminID: any) {
    this.router.navigate(['/userpage'], { queryParams: { adminID } });
  }
}
