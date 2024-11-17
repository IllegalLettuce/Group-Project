import {Component, inject} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {HttpClient} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {environment} from "../../environments/environment.development";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarComponent,
    FormsModule,
    NgForOf,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

  httpClient = inject(HttpClient);
  public data: Array<any> = [];
  buy: any;
  sell: any ;

  stocks = [
    { name: 'Lockheed Martin', buy: 0, sell: 0 },
    { name: 'Tesla', buy: 0, sell: 0 },
    { name: 'Apple', buy: 0, sell: 0 },
    // Add more companies as needed
  ];

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
    console.log(message);
    const myJSON = JSON.stringify(message);
    console.log(myJSON);

    const uri = environment.API_BASE_URL;

    this.httpClient.post(uri, myJSON)
      .subscribe({
        next: (data: any) => {
          this.data = data;
          console.log(data)
        }, error: (err) => console.log(err)
      });
  }

/////////////////////////end of file

}
