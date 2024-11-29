import { Component, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../environments/environment.development';

@Component({
  selector: 'app-paypal',
  standalone: true,
  templateUrl: './paypal.component.html',
  styleUrls: ['./paypal.component.css']
})
export class PaypalComponent implements AfterViewInit {
  amount: string = '20.00'; // Replace with dynamic value if needed
  clientID = environment.paypalID;

  constructor(private route: ActivatedRoute, private router: Router) {
    this.route.queryParams.subscribe(params => {
      if (params['amount']) {
        this.amount = params['amount'];
      }
    });
  }

  ngAfterViewInit(): void {
    const script = document.createElement('script');
    script.src = `https://www.paypal.com/sdk/js?client-id=${this.clientID}`;
    script.onload = () => {
      // @ts-ignore
      window.paypal.Buttons({
        createOrder: (data: any, actions: any) => {
          return actions.order.create({
            purchase_units: [
              {
                amount: {
                  value: this.amount
                }
              }
            ]
          });
        },
        onApprove: (data: any, actions: any) => {
          return actions.order.capture().then((details: any) => {
            alert(`Transaction completed by ${details.payer.name.given_name}`);
            this.router.navigate(['/registration'], { queryParams: { paymentSuccess: true } });
          });
        },
        onError: (err: any) => {
          console.error('PayPal error:', err);
        }
      }).render('#paypal-button-container');
    };
    document.body.appendChild(script);
  }
}

