import {Component, Inject, OnInit} from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatButton} from "@angular/material/button";
import {firstValueFrom, timeout} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../../environments/environment.development";
import {CommonModule} from "@angular/common";

@Component({
  selector: 'app-reportmodal',
  standalone: true,
  imports: [
    MatDialogContent,
    MatDialogActions,
    MatButton,
    MatDialogClose,
    MatDialogTitle,
    CommonModule
  ],
  templateUrl: './reportmodal.component.html',
  styleUrl: './reportmodal.component.css'
})
export class ReportmodalComponent implements OnInit{

  response_data: any;
  uri = environment.API_BASE_URL;
  isLoading: boolean = false;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { name: string }, private httpClient: HttpClient
  ) {}

  ngOnInit() {
    this.loadReportData();
  }

  async loadReportData(): Promise<void> {
    try {
      await this.generateReport(this.data.name);
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * Async function that is called by the modal to generate a report and show it on the modal.
   * Also controls the loading screen for the generation and the API call
   * @param name the name of the company that needs a report
   */
  async generateReport(name: string){
    this.isLoading = true;
    try{
      const uri_report = this.uri + '/report';
      const data = await firstValueFrom(
        this.httpClient.post(uri_report, {params: {name}}).pipe(timeout(20000))
      );
      this.response_data = data;
      console.log(data)
    }catch (error){
      console.log(error);
    } finally {
      this.isLoading = false;
    }
  };
}
