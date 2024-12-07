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
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {getAuth} from "firebase/auth";

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
    NgOptimizedImage
  ],
  templateUrl: './reportmodal.component.html',
  styleUrl: './reportmodal.component.css'
})
export class ReportmodalComponent implements OnInit{

  responseFromLLM: any;
  uri = environment.API_BASE_URL;
  isTheLLMLoading: boolean = false;
  ifAnErrorHasOccurred: boolean = false;


  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { name: string },
    private httpClient: HttpClient,
  ) {}

  /**
   * Calls to the API when modal is loaded
   */
  async ngOnInit() {
    const name = this.data.name
    const auth = getAuth();
    const user = auth.currentUser;
    const userID = user?.uid;
    console.log(userID);

    this.isTheLLMLoading = true;

    try {
      const uri_report = this.uri + '/report';
      this.responseFromLLM = await firstValueFrom(
        this.httpClient.post(uri_report, {params: {name, userID}})
          .pipe(timeout(120000))
      );
    } catch (error) {
      this.ifAnErrorHasOccurred = true;
    } finally {
      this.isTheLLMLoading = false;
    }
  }
}
