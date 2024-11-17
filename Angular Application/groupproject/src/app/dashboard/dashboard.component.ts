import {Component, inject} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {HttpClient} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {environment} from "../../environments/environment.development";
import {NgForOf} from "@angular/common";
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import {ReportmodalComponent} from "./modals/reportmodal/reportmodal.component";
import {CommonModule} from "@angular/common";

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
export class DashboardComponent {

  httpClient = inject(HttpClient);
  public data: Array<any> = [];
  buy: any;
  sell: any ;

  constructor(private dialog: MatDialog) {}

  stocks = [
    { name: 'Lockheed Martin', buy: 0, sell: 0 },
    { name: 'Tesla', buy: 0, sell: 0 },
    { name: 'Apple', buy: 0, sell: 0 },
    // Add more companies as needed
  ];

  openReportDialog(name: string){
    this.dialog.open(ReportmodalComponent, {
      width: '250px',
      data: { name: name }
    })
  }


    generateReport(name: String){
    console.log("Generating report for", name);
  }

  //takes stock data from the form
  submitStockData(stockName: String, buy: any, sell: any){
    this.sendToLLM(stockName, buy, sell, 1000)
  }

  //sends stock data to API as JSON
  sendToLLM(name:String, buy: any, sell: any, funds_dollar: any ){

    let message:JSON = <JSON><unknown>{
      "company": name,
      "buy_percent": buy,
      "sell_percent": sell,
      "funds_dollar": funds_dollar,
    };

    const uri = environment.API_BASE_URL;
    this.httpClient.post(uri, message)
      .subscribe({
        next: (data: any) => {
          this.data = data;
          console.log(data)
        }, error: (err) => console.log(err)
      });
  }

/////////////////////////end of file

}
