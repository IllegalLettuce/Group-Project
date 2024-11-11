import {Component, inject} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {HttpClient, HttpClientModule} from "@angular/common/http";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarComponent,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

  httpClient = inject(HttpClient);
  public data: Array<any> = [];


  ngOnInit(){

  }

  getStockNameFromUser(name: String){
    console.log(name)
    this.sendStockNameToLLM(name)
  }


  async sendStockNameToLLM(name:String){
    let message:JSON = <JSON><unknown>{
      "company": name
    }
    const myJSON = JSON.stringify(message);

    this.httpClient.post('https://quiet-yak-presently.ngrok-free.app', name)
      .subscribe({
        next: (data: any) => {
          console.log(data.blog);
          console.log(data.recommendation);
          this.data = data;
        }, error: (err) => console.log(err)
      });
  }







}
