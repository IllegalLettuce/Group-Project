import {Component, Inject} from '@angular/core';
import {environment} from "../../../../environments/environment.development";
import {MAT_DIALOG_DATA, MatDialogContent, MatDialogTitle} from "@angular/material/dialog";
import {HttpClient} from "@angular/common/http";
import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-managemodal',
  standalone: true,
  imports: [
    MatDialogContent,
    MatDialogTitle,
    CommonModule,
    FormsModule
  ],
  templateUrl: './managemodal.component.html',
  styleUrl: './managemodal.component.css'
})
export class ManagemodalComponent {
  uri = environment.API_BASE_URL;
  isSubmitted : boolean = false;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { name: string }, private httpClient: HttpClient
  ) {}


  submitData(){

    const buy = document.getElementById('buy');
    const sell = document.getElementById('sell');
    const funds_dollar = document.getElementById('funds_dollar');

    let message:JSON = <JSON><unknown>{
      "company": this.data.name,
      "buy_percent": buy,
      "sell_percent": sell,
      "funds_dollar": funds_dollar,
    };

    console.log(message);
    this.sendToLLM(message);
  }


  /**
   * Called by the modal to make the API call to the backend for the stock management.
   */
  sendToLLM(message: JSON){
    const uri_manage = this.uri + '/manage';
    try{
      this.httpClient.post(uri_manage, message)
        .subscribe({
          next: (data: any) => {
            console.log(data)
          }, error: (err) => console.log(err)
        });
    }catch(error){
      console.log(error)
    } finally {
      this.isSubmitted = true;
    }
  };
//////////////////////////////////////////////////////////
}
