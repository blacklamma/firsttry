import { Component, OnInit } from '@angular/core';
import { EmailService } from './email.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-email',
  templateUrl: './email.component.html',
  styleUrls: ['./email.component.css']
})
export class EmailComponent implements OnInit {

  outEmailData: any;
  inEmailData: any;
  page: number = 1;
  count: number = 0;
  tableSize: number = 25;
  outgoingEmailData: any = {};
  incomingEmailData: any = {};
  tabIndex: number = 0;
  constructor(private emailService: EmailService, private router: Router, 
    private route: ActivatedRoute, private location: Location, private toastr: ToastrService) {}

  ngOnInit(): void{
    this.fetchOutConf();
  }
  fetchOutEmails(): void {
    this.emailService.getOutEmails().subscribe(
      (response) => {
        this.outEmailData = response;
      }
    );
  }
  onTableDataChange(event: any) {
    this.page = event;
    this.fetchOutEmails();
  }
  onTableSizeChange(event: any): void {
    this.tableSize = event.target.value;
    this.page = 1;
    this.fetchOutEmails();
  }
  fetchOutConf(): void {
    this.emailService.getOutConf().subscribe(
      (response) => {
        this.outgoingEmailData = response;
        this.outgoingEmailData['host_password'] = '*****************';
      }
    );
  }
  public saveOutConf(): void{
    this.emailService.saveOutConf(this.outgoingEmailData).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Configurations have been saved', 'Success!');
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    )
  }


  fetchInEmails(): void {
    this.emailService.getInEmails().subscribe(
      (response) => {
        this.inEmailData = response;
      }
    );
  }
  onInTableDataChange(event: any) {
    this.page = event;
    this.fetchInEmails();
  }
  onInTableSizeChange(event: any): void {
    this.tableSize = event.target.value;
    this.page = 1;
    this.fetchInEmails();
  }
  fetchInConf(): void {
    this.emailService.getInConf().subscribe(
      (response) => {
        this.incomingEmailData = response;
        this.incomingEmailData['password'] = '*****************';
      }
    );
  }
  public saveInConf(): void{
    this.emailService.saveInConf(this.incomingEmailData).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Configurations have been saved', 'Success!');
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    )
  }

  changeTab(tabIndex: any): void{
    this.tabIndex = tabIndex;
    if(tabIndex == 0){
      this.fetchOutConf();
    }
    else if(tabIndex == 1){
      this.fetchOutEmails();
    }
    else if(tabIndex == 2){
      this.fetchInConf();
    }
    else if(tabIndex == 3){
      this.fetchInEmails();
    }
  }
  saveData(): void{
    if(this.tabIndex == 0){
      this.saveOutConf();
    }
    else if(this.tabIndex == 2){
      this.saveInConf();
    }
  }
  goBack(): void{
    this.location.back();
  }
}
