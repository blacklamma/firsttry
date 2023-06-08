import { Component, OnInit } from '@angular/core';
import { CustomerService } from './customer.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrls: ['./customer.component.css']
})
export class CustomerComponent implements OnInit {

  customerData: any;
  page: number = 1;
  count: number = 0;
  tableSize: number = 25;
  constructor(private customerService: CustomerService, private router: Router, private route: ActivatedRoute, private toastr: ToastrService) {}

  ngOnInit(): void{
    this.fetchCustomers();
  }
  fetchCustomers(): void {
    this.customerService.getCustomers().subscribe(
      (response) => {
        this.customerData = response;
      }
    );
  }
  onTableDataChange(event: any) {
    this.page = event;
    this.fetchCustomers();
  }
  onTableSizeChange(event: any): void {
    this.tableSize = event.target.value;
    this.page = 1;
    this.fetchCustomers();
  }
  addCustomer(): void{ 
    this.router.navigate(['add'], {relativeTo:this.route});
  }
  deleteCustomerConfirm(data: any): void{
    if(confirm("Are you sure to delete "+ data.email)) {
      this.deleteCustomer(data);
    }
  }
  deleteCustomer(data: any): void{ 
    this.customerService.deleteCustomer(data.id).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Customer deleted', 'Success!');
          this.fetchCustomers();
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }

}
