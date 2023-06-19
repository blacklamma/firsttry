import { Component, OnInit } from '@angular/core';
import { WorkflowService } from './workflow.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { ToastrService } from 'ngx-toastr';
import { Editor } from 'ngx-editor';
import { FormGroup, FormBuilder, ReactiveFormsModule, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-workflowform',
  templateUrl: './workflowform.component.html',
  styleUrls: ['./workflow.component.css']
})
export class WorkflowformComponent {

  event: any = 'add';
  id: any;
  public wfData !: FormGroup;
  ownerOptions = [{'name': '', 'id': null}];
  stateOptions: any = [];
  statusOptions: any = {};
  stateNameData: any = {};
  statusNameData: any = {};
  statusDataList: any = [];
  ruleDataList: any = [];
  notifDataList: any = [];
  statusOptionsList: any = [];
  editor: Editor;
  constructor(private formBuilder : FormBuilder, private workflowService: WorkflowService, private router: Router, 
    private route: ActivatedRoute, private location: Location, private toastr: ToastrService) {}

  ngOnInit(): void{
    this.editor = new Editor();
    this.event = this.route.snapshot.paramMap.get('event');
    this.id = this.route.snapshot.paramMap.get('id');
    this.wfData = this.formBuilder.group({
      id: [''],
      name: ['', Validators.required],
      owners: [[]],
    })
    
    this.workflowService.getWorkflowOptions(this.id).subscribe(
      (response) => {
        this.ownerOptions = response.owner_options;
        this.stateOptions = response.state_options || [];
        for(let i=0; i<this.stateOptions.length; i++){
          this.stateNameData[this.stateOptions[i].id] = this.stateOptions[i].name;
        }
        this.statusOptionsList = response.status_options || [];
        console.log(this.statusOptionsList)
        for(let i=0; i<this.statusOptionsList.length; i++){
          this.statusNameData[this.statusOptionsList[i].id] = this.statusOptionsList[i].name;
          if(this.statusOptions[this.statusOptionsList[i].state] == undefined){
            this.statusOptions[this.statusOptionsList[i].state] = [{'id': this.statusOptionsList[i].id, 'name': this.statusOptionsList[i].name}]
          }
          else{
            this.statusOptions[this.statusOptionsList[i].state].push({'id': this.statusOptionsList[i].id, 'name': this.statusOptionsList[i].name})
          }
        }
        this.getEditData();
      }
    );
  }
  getEditData(): void{
    if(this.id != 0 && this.id != undefined){
      this.event = 'edit';
      this.workflowService.getWorkflow(this.id).subscribe(
        (response) => {
          this.wfData.setValue({
            id: response.id,
            name: response.name,
            owners: response.owners,
          });
        }
      );
      this.workflowService.getStatuses(this.id).subscribe(
        (response) => {
          this.statusDataList = response;
        }
      );
      this.workflowService.getRules(this.id).subscribe(
        (response) => {
          this.ruleDataList = response;
          for(let i=0; i<this.ruleDataList.length; i++){
            this.changeIfState(this.ruleDataList[i].if_state, i);
            this.changeIfStatus(this.ruleDataList[i].if_status, i);
            this.changeThenState(this.ruleDataList[i].then_state, i);
            this.changeThenStatus(this.ruleDataList[i].then_status, i);
          }
        }
      );
      this.workflowService.getNotifs(this.id).subscribe(
        (response) => {
          this.notifDataList = response;
          for(let i=0; i<this.notifDataList.length; i++){
            this.changeNotifState(this.notifDataList[i].state, i);
            this.changeNotifStatus(this.notifDataList[i].status, i);
          }
        }
      );
    }
  }
  addStatus(): void{
    this.statusDataList.push({'stateName': 'Open', 'stateId': 1, 'statusName': '', 'stage': '', 'wfId': this.id});
  }
  changeIfState(state_id: number, index: number): void{
    this.ruleDataList[index]['ifStateName'] = this.stateNameData[state_id];
    this.ruleDataList[index]['ifStatusOptions'] = this.statusOptions[state_id] || [];
  }
  changeIfStatus(status_id: number, index: number): void{
    this.ruleDataList[index]['ifStatusName'] = this.statusNameData[status_id];
  }
  changeThenState(state_id: number, index: number): void{
    this.ruleDataList[index]['thenStateName'] = this.stateNameData[state_id];
    this.ruleDataList[index]['thenStatusOptions'] = this.statusOptions[state_id] || [];
  }
  changeThenStatus(status_id: number, index: number): void{
    this.ruleDataList[index]['thenStatusName'] = this.statusNameData[status_id];
  }
  changeNotifState(state_id: number, index: number): void{
    this.notifDataList[index]['stateName'] = this.stateNameData[state_id];
    this.notifDataList[index]['statusOptions'] = this.statusOptions[state_id] || [];
  }
  changeNotifStatus(status_id: number, index: number): void{
    this.notifDataList[index]['statusName'] = this.statusNameData[status_id];
  }
  saveStatus(statusData: any, index: number): void{
    this.workflowService.saveStatus(statusData).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Status has been saved', 'Success!');
          this.statusDataList[index]['stateName'] = response.data.state_name;
          this.statusDataList[index]['name'] = statusData['status_temp'];
          this.statusDataList[index]['stage'] = statusData['stage_temp'];
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
  addRule(): void{
    this.ruleDataList.push({'ruleName': '', 'rule': '', 'wfId': this.id});
  }
  saveRule(ruleData: any, index: number): void{
    this.workflowService.saveRule(ruleData).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Rule has been saved', 'Success!');
          this.ruleDataList[index]['name'] = ruleData['name_temp'];
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
  addNotif(): void{
    this.notifDataList.push({'notifSubject': '', 'notifBody': '', 'wfId': this.id});
  }
  saveNotif(notifData: any, index: number): void{
    this.workflowService.saveNotif(notifData).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Notif has been saved', 'Success!');
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
  saveWorkflow(): void{ 
    this.workflowService.saveWorkflow(this.wfData.value).subscribe(
      (response) => {
        if(response.status == 'success'){
          let id = response.data.id;
          this.toastr.success('Workflow data has been saved', 'Success!');
          if(this.event == 'add'){
            // this.router.navigate(['workflow/edit/' + id]);
            this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
                this.router.navigate(['workflow/edit/' + id]);
            });
          }
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
  changeTab(tabIndex: any): void{
  }

  goBack(): void{
    this.router.navigate(['workflow']);
  }
}
