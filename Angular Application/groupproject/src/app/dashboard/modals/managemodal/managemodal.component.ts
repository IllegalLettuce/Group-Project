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
    @Inject(MAT_DIALOG_DATA) public data: { name: string, ticker: string, adminID: any },
    private http: HttpClient,
    private builder: FormBuilder
  ) {
    this.manageForm = this.builder.group({
      buy: ['',
        [Validators.required],
      ],
      sell: ['',
        [Validators.required],
      ],
      funds_dollar: ['',
        [Validators.required]
      ],
    });
  }

  /**
   * Format percentage input
   */
  formatPercentageInput(formField: string) {
    let value = this.manageForm.get(formField)?.value;
    value = value.replace(/\D/g, '');
    let numericValue = Number(value);
    if (numericValue < 1) {
      numericValue = 1;
    } else if (numericValue > 100) {
      numericValue = 100;
    }
    value = numericValue.toString();
    value = value + '%';
    this.manageForm.get(formField)?.setValue(value, { emitEvent: false });
  }


  /**
   * Form USD funds
   */  // Format the input value to US dollar format and prepend the '$'
  formatCurrencyInput() {
    let value = this.manageForm.get('funds_dollar')?.value;
    let value_percent = "";
    value = value.replace(/[^\d.-]/g, '');
    if (value) {
      value = Number(value).toLocaleString('en-US');
      value_percent = '$' + value;
      this.manageForm.get('funds_dollar')?.setValue(value_percent, { emitEvent: false });
    }
  }

  /**
   * Called by the modal to make the API call to the backend for the stock management.
   */
  sendToLLM(){
    const uri_manage = this.uri + '/manage';
    let {buy, sell, funds_dollar} = this.manageForm.value;
    let message:JSON = <JSON><unknown>{
      "userID" : this.data.adminID,
      "company": this.data.name,
      "ticker": this.data.ticker,
      "buy_percent": buy,
      "sell_percent": sell,
      "funds_dollar": funds_dollar,
    };
    let messageString = JSON.stringify(message)
    try{
      this.http.post(uri_manage, messageString)
        .subscribe({
          next: (data: any) => {
          }, error: () => this.ifError = true
        });
      this.isSubmitted = true;
    }catch(error){
      this.ifError = true;
      if (error instanceof HttpErrorResponse){
        console.log("Unable to connect to the server. Please check your connection");
      }
    }
  };
}
