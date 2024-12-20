import {Component, Inject, OnInit} from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent, MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatButton, MatIconButton} from "@angular/material/button";
import {firstValueFrom, timeout} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../../environments/environment.development";
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {getAuth} from "firebase/auth";
import {MatIcon} from "@angular/material/icon";
import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import {MatProgressBar} from "@angular/material/progress-bar";

@Component({
  selector: 'app-reportmodal',
  standalone: true,
  imports: [
    MatDialogContent,
    MatDialogActions,
    MatButton,
    MatDialogClose,
    MatDialogTitle,
    CommonModule,
    NgOptimizedImage,
    MatIconButton,
    MatIcon,
    MatProgressBar
  ],
  templateUrl: './reportmodal.component.html',
  styleUrl: './reportmodal.component.css'
})
export class ReportmodalComponent implements OnInit {
  responseFromLLM: any;
  uri = environment.API_BASE_URL;
  isTheLLMLoading: boolean = false;
  ifAnErrorHasOccurred: boolean = false;
  progressBar: number = 0;
  progressInterval: any;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { name: string },
    private httpClient: HttpClient,
    public dialogRef: MatDialogRef<ReportmodalComponent>
  ) {}

  ngOnInit() {
    const name = this.data.name;
    this.completelyRealAndNotFakeLoadingBar();
    this.fetchData(name);
  }

  /**
   * Loading Bar for the API call for UX
   */
  completelyRealAndNotFakeLoadingBar() {
    this.progressBar = 0;
    this.isTheLLMLoading = true;
    this.dialogRef.disableClose = true;

    this.progressInterval = setInterval(() => {
      if (this.progressBar < 80) {
        this.progressBar += Math.floor(Math.random() * (8 - 2 + 1)) + 2;
      }
      else if (this.progressBar > 80){
        console.log()
      }
      else {
        clearInterval(this.progressInterval);
      }
    }, (Math.floor(Math.random() * (4000 - 2000 + 1)) + 2000));
  }

  /**
   * Generates report from the API
   * @param name
   */
  async fetchData(name: string) {
    try {
      const uri_report = `${this.uri}/report`;
      this.responseFromLLM = await firstValueFrom(
        this.httpClient.post(uri_report, { params: { name } })
          .pipe(timeout(120000))
      );
    } catch (error) {
      this.ifAnErrorHasOccurred = true;
    } finally {
      this.isTheLLMLoading = false;
      this.dialogRef.disableClose = false;
      clearInterval(this.progressInterval);
    }
  }

  /**
   * Pdf download for the LLM report
   */
  downloadResponseAsPDF() {
    const auth = getAuth();
    const doc = new jsPDF();

    doc.setFontSize(16);
    doc.text(`Report: ${this.data.name}`, 10, 10);

    doc.setFontSize(10);
    doc.text(`Date: ${this.responseFromLLM.date}`, 10, 20);
    doc.text(`Name: ${auth.currentUser?.displayName || 'Unknown'}`, 10, 30);

    let yOffset = 40;
    doc.text('Brief:', 10, yOffset);
    yOffset += 10;
    doc.setFontSize(10);
    const blogLines = doc.splitTextToSize(this.responseFromLLM.blog || 'Data not found', 180);
    doc.text(blogLines, 10, yOffset);

    yOffset += blogLines.length * 10 + 10; // Adjust spacing after the blog
    const extendedBlogLines = doc.splitTextToSize(this.responseFromLLM.extended_blog || 'Data not found', 180);
    doc.text(extendedBlogLines, 10, yOffset);

    yOffset += extendedBlogLines.length * 10 + 20; // Adjust spacing for the table
    const recommendations = [
      ['Buy', this.responseFromLLM.recommendation.buy || 'Data not found'],
      ['Sell', this.responseFromLLM.recommendation.sell || 'Data not found'],
      ['Hold', this.responseFromLLM.recommendation.hold || 'Data not found'],
    ];

    autoTable(doc, {
      head: [['Recommendation', 'Threshold']],
      body: recommendations,
      startY: yOffset,
      theme: 'grid',
    });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    doc.save(`report_${this.data.name}_${timestamp}.pdf`);
  }

  /**
   * For the exit button on the dialog
   */
  closeModal() {
      this.dialogRef.close();
  }

}
