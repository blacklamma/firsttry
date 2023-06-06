import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  userData: any;
  page: number = 1;
  count: number = 0;
  tableSize: number = 25;
  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute, private toastr: ToastrService) {}

  ngOnInit(): void{
    this.fetchUsers();
  }
  fetchUsers(): void {
    this.userService.getUsers().subscribe(
      (response) => {
        this.userData = response;
      }
    );
  }
  onTableDataChange(event: any) {
    this.page = event;
    this.fetchUsers();
  }
  onTableSizeChange(event: any): void {
    this.tableSize = event.target.value;
    this.page = 1;
    this.fetchUsers();
  }
  addUser(): void{ 
    this.router.navigate(['add'], {relativeTo:this.route});
  }
  deleteUserConfirm(data: any): void{
    if(confirm("Are you sure to delete "+ data.username)) {
      this.deleteUser(data);
    }
  }
  deleteUser(data: any): void{ 
    this.userService.deleteUser(data.id).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('User deleted', 'Success!');
          this.fetchUsers();
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }

}
