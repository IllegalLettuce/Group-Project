import {Component, Inject} from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatButton} from "@angular/material/button";

@Component({
  selector: 'app-reportmodal',
  standalone: true,
  imports: [
    MatDialogContent,
    MatDialogActions,
    MatButton,
    MatDialogClose,
    MatDialogTitle
  ],
  templateUrl: './reportmodal.component.html',
  styleUrl: './reportmodal.component.css'
})
export class ReportmodalComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { name: string }) {}
}
