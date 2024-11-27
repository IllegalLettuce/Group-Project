import {Component, Inject} from '@angular/core';
import {environment} from "../../../../environments/environment.development";
import {MAT_DIALOG_DATA, MatDialogContent, MatDialogTitle} from "@angular/material/dialog";
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {CommonModule} from "@angular/common";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-managemodal',
  standalone: true,
  imports: [
    MatDialogContent,
    MatDialogTitle,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './managemodal.component.html',
  styleUrl: './managemodal.component.css'
})
export class ManagemodalComponent {
  uri = environment.API_BASE_URL;
  isSubmitted : boolean = false;
  ifError: boolean = false;
  manageForm: FormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { name: string, ticker: string },
    private httpClient: HttpClient,
    private builder: FormBuilder
  ) {
    this.manageForm = this.builder.group({
      buy: ['',
        [Validators.required,
          Validators.pattern(/^100(\.0{1,2})?$|^\d{1,2}(\.\d{1,2})?$/)],
      ],
      sell: ['',
        [Validators.required,
          Validators.pattern(/^100(\.0{1,2})?$|^\d{1,2}(\.\d{1,2})?$/)],
      ],
      funds_dollar: ['',
        [Validators.required,
          Validators.pattern(/^\$?([1-9]\d{0,2}(,\d{3})*|0)(\.\d{1,2})?$/)]
      ],
    });
  }

  /**
   * Called by the modal to make the API call to the backend for the stock management.
   */
  sendToLLM(){
    const uri_manage = this.uri + '/manage';
    const {buy, sell, funds_dollar} = this.manageForm.value;
    let message:JSON = <JSON><unknown>{
      "company": this.data.name,
      "ticker": this.data.ticker,
      "buy_percent": buy ,
      "sell_percent": sell,
      "funds_dollar": funds_dollar,
    };
    try{
      this.httpClient.post(uri_manage, message)
        .subscribe({
          next: (data: any) => {
          }, error: () => this.ifError = true
        });
      this.isSubmitted = true;
    }catch(error){
      this.ifError = true;
      if (error instanceof HttpErrorResponse){
        console.log("Unable to connect to the server. Please check your connection")
      }
    }
  };
//////////////////////////////////////////////////////////
}
