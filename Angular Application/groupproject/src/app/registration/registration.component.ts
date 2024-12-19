import {ChangeDetectorRef, Component, NgZone, OnInit} from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { environment } from '../../environments/environment.development';
import {HttpClient} from "@angular/common/http";
import {getAuth, signInWithEmailAndPassword} from "firebase/auth";
import {NgIf} from "@angular/common";


@Component({
  selector: 'app-registration',
  standalone: true,
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css'],
  imports: [ReactiveFormsModule, NgIf]
})
export class RegistrationComponent implements OnInit {
  registerForm: FormGroup;
  StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;
  paymentSuccess: boolean = false;

  constructor(
    private builder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private cdRef: ChangeDetectorRef,
    private http: HttpClient
  ) {
    this.registerForm = this.builder.group({
      name: ['', Validators.required],
      surname: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]], //Validators.pattern(this.StrongPasswordRegx)
      confirmPassword: ['', Validators.required],
      userType: ['', Validators.required],
      companyName: [''],
      adminEmail: [''],
      funds: ['']
    }, {
      validators: this.ConfirmedValidator("password", "confirmPassword")
    });
  }

  ngOnInit(): void {
    const navigation = this.router.getCurrentNavigation();
    const state = navigation?.extras.state as { formData: any };

    if (state?.formData) {
      console.log("Data found in router state");
      this.registerForm.setValue(state.formData);
      this.cdRef.detectChanges();
    } else {
      const savedFormData = sessionStorage.getItem('formData');
      if (savedFormData) {
        console.log("Data found in sessionStorage");
        this.registerForm.setValue(JSON.parse(savedFormData));
        this.cdRef.detectChanges();
      }
    }

    this.route.queryParams.subscribe(params => {
      this.paymentSuccess = params["paymentSuccess"] === "true";

      if (this.paymentSuccess && this.registerForm.valid) {
        console.log("Payment success, proceeding with user registration.");
        this.registerUser();
      } else if (!this.registerForm.valid) {
        console.error("Form is not valid");
      } else if (!this.paymentSuccess) {
        console.log("Payment not completed.");
      }
    });
  }


  /**
   * Different inputs for admin or manager in the form
   */
  adminOrManager(): void {
    const userType = this.registerForm.get('userType')?.value;
    if (userType === 'admin') {
      this.registerForm.get('companyName')?.setValidators(Validators.required);
      this.registerForm.get('adminEmail')?.clearValidators();
    } else if (userType === 'manager') {
      this.registerForm.get('adminEmail')?.setValidators([Validators.required, Validators.email]);
      this.registerForm.get('companyName')?.clearValidators();
    } else {
      this.registerForm.get('companyName')?.clearValidators();
      this.registerForm.get('adminEmail')?.clearValidators();
    }
    this.registerForm.get('companyName')?.updateValueAndValidity();
    this.registerForm.get('adminEmail')?.updateValueAndValidity();
  }

  /**
   * Validators for the password form
   * @param controlName
   * @param matchingControlName
   * @constructor
   */
  ConfirmedValidator(controlName: string, matchingControlName: string) {
    return (formGroup: FormGroup) => {
      const control = formGroup.controls[controlName];
      const matchingControl = formGroup.controls[matchingControlName];
      if (
        matchingControl.errors &&
        !matchingControl.errors["confirmedValidator"]
      ) {
        return;
      }
      if (control.value !== matchingControl.value) {
        matchingControl.setErrors({ confirmedValidator: true });
      } else {
        matchingControl.setErrors(null);
      }
    };
  }

  /**
   * Goes to Paypal from the form
   */
  goToPayPal() {
    let paymentAmount = 100.00;

    if (this.registerForm.get('userType')?.value === 'admin') {
      const funds = parseFloat(this.registerForm.get('funds')?.value || '0');
      paymentAmount += funds;
    }

    sessionStorage.setItem('formData', JSON.stringify(this.registerForm.value));
    this.router.navigate(['/paypal'], {
      queryParams: { amount: paymentAmount.toFixed(2) }
    });
  }


  /**
   * Register user when back from paypal
   */
  registerUser() {
    const formData = this.registerForm.value;
    const uri_create_user = environment.API_BASE_URL + '/createuser'
    const auth = getAuth()
    const { email, password } = formData;
    this.http.post(uri_create_user, formData)
      .subscribe({
        next: (response: any) => {
          if (response.message === 'created') {
            signInWithEmailAndPassword(auth, email, password).then(
              (userCredential)=>{
                const user = userCredential
                this.router.navigate(['/dashboardmanager']);
              }
            )
          } else {
            console.error('User creation failed:', response);
          }
        },
        error: (err) => {
          console.error('Error during API call:', err);
        }
      });
  }
}

