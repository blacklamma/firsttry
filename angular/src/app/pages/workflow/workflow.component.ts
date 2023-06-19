import { Component, OnInit } from '@angular/core';
import { WorkflowService } from './workflow.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-workflow',
  templateUrl: './workflow.component.html',
  styleUrls: ['./workflow.component.css']
})
export class WorkflowComponent implements OnInit {

  wfData: any;
  page: number = 1;
  count: number = 0;
  tableSize: number = 25;
  constructor(private workflowService: WorkflowService, private router: Router, 
    private route: ActivatedRoute, private location: Location, private toastr: ToastrService) {}

  ngOnInit(): void{
    this.fetchWorkflows();
  }
  fetchWorkflows(): void {
    this.workflowService.getWorkflows().subscribe(
      (response: any) => {
        this.wfData = response;
      }
    );
  }
  onTableDataChange(event: any) {
    this.page = event;
    this.fetchWorkflows();
  }
  onTableSizeChange(event: any): void {
    this.tableSize = event.target.value;
    this.page = 1;
    this.fetchWorkflows();
  }
  addWorkflow(): void{ 
    this.router.navigate(['add/0'], {relativeTo:this.route});
  }
  deleteWfConfirm(data: any): void{
    if(confirm("Are you sure to delete "+ data.username)) {
      this.deleteWorkflow(data);
    }
  }
  deleteWorkflow(data: any): void{ 
    this.workflowService.deleteWorkflow(data.id).subscribe(
      (response: any) => {
        if(response.status == 'success'){
          this.toastr.success('Workflow deleted', 'Success!');
          this.fetchWorkflows();
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
}