  import {Component, OnInit} from '@angular/core';
  import {NavbarComponent} from "../navbar/navbar.component";
  import {getAuth} from "firebase/auth";
  import {UserCheckService} from "../services/user-check.service";
  import {NgForOf, NgIf} from "@angular/common";
  import {HttpClient} from "@angular/common/http";
  import {environment} from "../../environments/environment.development";

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
    constructor(
      private userCheck: UserCheckService,
      private http: HttpClient
    ) {}

    async ngOnInit() {
      this.isAdmin  = false;
      this.isManager = false;

      const auth = getAuth();
      const user = auth.currentUser;
      const userID = user?.uid;
      if (userID != null) {
        this.isAdmin = await this.userCheck.isUserAnAdmin(userID);
        this.isManager = await this.userCheck.isUserAnManager(userID);
        this.userFunds = await this.userCheck.getUserFunds(userID);
      }
      if (this.isAdmin){
        await this.fetchUserStocks(user);
      }

    }


    /**
     * Fetches all the stocks being managed by a user
     * @param user
     */
    async fetchUserStocks(user: any){
      const uri_fetchStocks = environment.API_BASE_URL + "/managedstocks"
      const userID = user.uid
      this.http.post<any[]>(uri_fetchStocks, {userID}).subscribe(
        response=>{
          this.managedStocks = response;
          console.log(this.managedStocks);
        }
      )
    }
  }

