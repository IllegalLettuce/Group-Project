import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {FormsModule} from "@angular/forms";
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import {ReportmodalComponent} from "./modals/reportmodal/reportmodal.component";
import {CommonModule} from "@angular/common";
import {ManagemodalComponent} from "./modals/managemodal/managemodal.component";
import {environment} from '../../environments/environment.development';
import {HttpClient} from "@angular/common/http";
import {getAuth} from "firebase/auth";
import {ActivatedRoute} from "@angular/router";
import {UserCheckService} from "../services/user-check.service";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarComponent,
    FormsModule,
    NgForOf,
    MatDialogModule,
    CommonModule,
    NgOptimizedImage
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})

export class DashboardComponent implements OnInit {
  adminID: string | null = null;
  public data: any;
  stocks: {
    name: string,
    ticker: string
  }[] = [];
  userFunds: any

  constructor(
    private dialog: MatDialog,
    private http: HttpClient,
    private route: ActivatedRoute,
    private userCheck: UserCheckService
  ) {}

  async ngOnInit() {
    const uriGetStocks = environment.API_BASE_URL + '/getstocks';
    const requestBody = {};
    const auth = getAuth();
    const currentUserID = auth.currentUser?.uid;


    this.route.queryParams.subscribe(async params => {
      if (params['adminID']) {
        this.adminID = params['adminID'];
      } else if (currentUserID && await this.userCheck.isUserAnAdmin(currentUserID)) {
        this.adminID = currentUserID;
      }
    });

    this.http.post<any[]>(uriGetStocks, requestBody).subscribe(
      (response) => {
        this.stocks = response;
      }
    );
  }


  /**
   * Controls the report dialog from the frontend
   * @param name
   */
  openReportDialog(name: string) {
    const dialogRef = this.dialog.open(ReportmodalComponent, {
      width: '30em',
      data: { name: name }
    });
    dialogRef.afterClosed().subscribe(() => {
    });
  }

  /**
   * Controls the manage stocks dialog from the frontend
   * @param name
   * @param ticker
   */
  openManageDialog(name: string, ticker: string) {
    this.dialog.open(ManagemodalComponent, {
      width: '30em',
      data: {
        name: name,
        ticker: ticker,
        adminID: this.adminID
      }
    });
  }

}
