import {Component, OnInit} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {FormsModule} from "@angular/forms";
import {NgForOf, NgOptimizedImage} from "@angular/common";
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
    CommonModule,
    NgOptimizedImage
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})

export class DashboardComponent implements OnInit {
  public data: any;
  stocks: {
    graphUrl: any;
    name: string, ticker: string }[] = [];

  constructor(private dialog: MatDialog, private http: HttpClient) {}

  ngOnInit(): void {
    const uriGetStocks = environment.API_BASE_URL + '/getstocks';
    const requestBody = {};
    this.http.post<any[]>(uriGetStocks, requestBody).subscribe(
      (response) => {
        this.stocks = response;
        this.generateStockGraphs();
      }
    );
  }

  /**
   * Creates the stock graphs for the dashboard
   */
  generateStockGraphs() {
    const uri_graphs = environment.API_BASE_URL + "/generate_graphs";
    const requestBody = { stocks: this.stocks };
    this.http.post<{ status: string, graphs: Record<string, string> }>(uri_graphs, requestBody)
      .subscribe(response => {
        if (response.status === 'success') {
          this.updateStockGraphs(response.graphs);
        }
      });
  }

  /**
   * Updates the stocks for the dashboard
   * @param graphs
   */
  updateStockGraphs(graphs: Record<string, string>) {
    this.stocks = this.stocks.map(stock => {
      const graphUrl = graphs[stock.name]
        ? `${environment.API_BASE_URL}/graphs/${graphs[stock.name]}`
        : undefined;
      return { ...stock, graphUrl };
    });
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
      data: { name: name, ticker: ticker }
    });
  }
}
