import {Component, Inject} from '@angular/core';
import {environment} from "../../../../environments/environment.development";
import {MAT_DIALOG_DATA, MatDialogContent, MatDialogTitle} from "@angular/material/dialog";
import {HttpClient} from "@angular/common/http";
import {CommonModule} from "@angular/common";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-managemodal',
  standalone: true,
  imports: [
    MatDialogContent,
    MatDialogTitle,
    CommonModule,
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './managemodal.component.html',
  styleUrl: './managemodal.component.css'
})
export class ManagemodalComponent {
  uri = environment.API_BASE_URL;
  isSubmitted : boolean = false;
  manageForm: FormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { name: string, ticker: string },
    private httpClient: HttpClient,
    private builder: FormBuilder
  ) {
    this.manageForm = this.builder.group({
      buy: ['', [Validators.required, Validators.min(0), Validators.max(100)]],
      sell: ['', [Validators.required, Validators.min(0), Validators.max(100)]],
      funds_dollar: ['', [Validators.required, Validators.min(1)]]
    })
  }

  submitData(){
    const {buy, sell, funds_dollar} = this.manageForm.value;
    let message:JSON = <JSON><unknown>{
      "company": this.data.name,
      "ticker": this.data.ticker,
      "buy_percent": buy ,
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
