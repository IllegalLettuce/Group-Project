import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { getAuth, createUserWithEmailAndPassword } from 'firebase/auth';

@Component({
  selector: 'app-registration',
  standalone: true,
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css'],
  imports: [ReactiveFormsModule]
})
export class RegistrationComponent implements OnInit {
  registerForm: FormGroup;
  StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;
  paymentSuccess: boolean = false;

  constructor(
    private builder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.registerForm = this.builder.group({
      name: ['', Validators.required],
      surname: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.pattern(this.StrongPasswordRegx)]],
      confirmPassword: ['', Validators.required]
    }, {
      validators: this.ConfirmedValidator("password", "confirmPassword")
    });
  }

  ngOnInit(): void {
    const savedFormData = localStorage.getItem("registrationForm");
    if (savedFormData) {
      this.registerForm.setValue(JSON.parse(savedFormData));
    }

    this.route.queryParams.subscribe(params => {
      this.paymentSuccess = params["paymentSuccess"] === "true";
      if (this.paymentSuccess) {
        this.registerUser();
      }
    });
  }

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

  goToPayPal() {
    localStorage.setItem("registrationForm", JSON.stringify(this.registerForm.value));
    const paymentAmount = "20.00"; // Replace with dynamic amount if needed
    this.router.navigate(["/paypal"], { queryParams: { amount: paymentAmount } });
  }

  registerUser() {
    if (!this.paymentSuccess) {
      alert("Payment not completed. Please pay first.");
      return;
    }


    const { email, password } = this.registerForm.value;
    console.log(email);
    const auth = getAuth();
    createUserWithEmailAndPassword(auth, email, password)
      .then(result => {
        localStorage.removeItem('registrationForm');
        window.location.replace("/dashboard");
      })
      .catch(console.log);
  }
}

