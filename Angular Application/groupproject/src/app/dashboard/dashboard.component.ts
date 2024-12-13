import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import {ReportmodalComponent} from "./modals/reportmodal/reportmodal.component";
import {CommonModule} from "@angular/common";
import {ManagemodalComponent} from "./modals/managemodal/managemodal.component";
import { environment } from '../../environments/environment.development';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarComponent,
    FormsModule,
    NgForOf,
    MatDialogModule,
    CommonModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})

export class DashboardComponent implements OnInit {
  public data: any;
  stocks: { name: string, ticker: string }[] = [];
  isTheLLMLoading: boolean = false;

  constructor(private dialog: MatDialog, private http: HttpClient) {}

  ngOnInit(): void {
    const uri_getstocks = environment.API_BASE_URL + '/getstocks';
    const requestBody = {};
    this.http.post<any[]>(uri_getstocks, requestBody).subscribe(
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
      width: '28em',
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
      width: '28em',
      data: { name: name, ticker: ticker }
    });
  }
}
