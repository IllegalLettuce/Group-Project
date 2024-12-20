  import {Component, OnInit} from '@angular/core';
  import {NavbarComponent} from "../navbar/navbar.component";
  import {getAuth} from "firebase/auth";
  import {UserCheckService} from "../services/user-check.service";
  import {NgForOf, NgIf} from "@angular/common";
  import {HttpClient} from "@angular/common/http";
  import {environment} from "../../environments/environment.development";
  import {ActivatedRoute} from "@angular/router";

  @Component({
    selector: 'app-userpage',
    standalone: true,
    imports: [
      NavbarComponent,
      NgIf,
      NgForOf
    ],
    templateUrl: './userpage.component.html',
    styleUrl: './userpage.component.css'
  })
  export class UserpageComponent implements OnInit {
    isAdmin: boolean  | undefined;
    isManager: boolean | undefined;
    userFunds: any;
    managedStocks: {
      buy_percent: number;
      company: string;
      funds_dollar: number;
      sell_percent: number;
      shares_owned: number;
      ticker: string;
    }[] = [];
    adminID: string | null = null;

    constructor(
      private userCheck: UserCheckService,
      private http: HttpClient,
      private route: ActivatedRoute
    ) {}

    async ngOnInit() {
      this.isAdmin  = false;
      this.isManager = false;

      const auth = getAuth();
      const currentUserID = auth.currentUser?.uid || null;

      this.route.queryParams.subscribe(async params => {
        if (params['adminID']) {
          this.adminID = params['adminID'];
        } else if (currentUserID) {
          this.adminID = currentUserID;
        }

        if (!this.adminID) {
          console.error("Admin ID could not be determined.");
        } else {
          await this.getUserDetails();
          await this.fetchUserStocks();
        }
      });

    }

    /**
     * Fetches admin and manager status for the current adminID
     */
    async getUserDetails() {
      if (this.adminID) {
        this.isAdmin = await this.userCheck.isUserAnAdmin(this.adminID);
        this.isManager = await this.userCheck.isUserAnManager(this.adminID);
        this.userFunds = await this.userCheck.getUserFunds(this.adminID);
      }
    }


    /**
     * Fetches all the stocks being managed by the admin
     */
    async fetchUserStocks(){
      const uri_fetchStocks = environment.API_BASE_URL + "/managedstocks"
      const userID = this.adminID
      this.http.post<any[]>(uri_fetchStocks, {userID}).subscribe(
        response=>{
          this.managedStocks = response;
        }
      )
    }
  }

