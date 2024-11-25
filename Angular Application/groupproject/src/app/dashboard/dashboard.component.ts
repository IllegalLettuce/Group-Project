import {Component} from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import {ReportmodalComponent} from "./modals/reportmodal/reportmodal.component";
import {CommonModule} from "@angular/common";
import {ManagemodalComponent} from "./modals/managemodal/managemodal.component";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarComponent,
    FormsModule,
    NgForOf,
    MatDialogModule,
    CommonModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

  public data:any;

  //Temporary stocks data
  stocks = [
    {name: "Lockheed Martin", ticker: "NYSE:LMT"},
    {name: "General Dynamics", ticker: "NYSE: GD"},
    {name: "Northrop Grumman", ticker: "NYSE: NOC"},
    {name: "Rtx", ticker: "NYSE: RTX"},
    {name: "Boeing", ticker: "NYSE: BA"},
    {name: "L3Harris", ticker: "NYSE: LHX"},
    {name: "Rheinmetall", ticker: "ETR: RHM"},
    {name: "SAAB", ticker: "STO: SAAB-B"},
    {name: "Hensoldt", ticker: "ETR: HAG"},
    {name: "Leonardo", ticker: "BIT: LDO"}
  ];

  constructor(private dialog: MatDialog) {}

  /**
   * Controls the report dialog from the frontend
   * @param name
   */
  openReportDialog(name: string){
    this.dialog.open(ReportmodalComponent, {
      width: '28em',
      data: { name: name }
    })
  };

  /**
   * Controls the manage stocks dialog from the frontend
   * @param name
   * @param ticker
   */
  openManageDialog(name: string, ticker: string){
    this.dialog.open(ManagemodalComponent, {
      width: '28em',
      data: { name: name, ticker: ticker }
    })
  }
/////////////////////////end of file
}
