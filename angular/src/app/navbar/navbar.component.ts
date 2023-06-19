import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router'
import { FormGroup, FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { GlobalComponent } from '../global-component';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  profilePictureData = '';
  isStaff = false;
  permissions : any;
  
  public logOutForm !: FormGroup;
  constructor(private formBuilder : FormBuilder, private http: HttpClient, private router: Router, private toastr: ToastrService){}
  ngOnInit(): void{
    this.logOutForm = this.formBuilder.group({
      username: [''],
      password: ['']
    });
    this.profilePictureData = localStorage.getItem('avatar') || '';
    this.isStaff = this.getBoolean(localStorage.getItem('isStaff'));
    this.permissions = JSON.parse(localStorage.getItem('permissions') || "{}");
  }
  logOut(){
    this.http.post(GlobalComponent.appUrl + 'user/logout/', {username: localStorage.getItem('username')}, {responseType: 'text'})
    .subscribe(
      (resData) => {
        console.log(resData)
        localStorage.setItem('username', '');
        localStorage.setItem('isLoggedIn', 'false');
        this.toastr.success('Logged Out!', resData);
        this.router.navigate(['']);
      }
    )
  }

  private getBoolean(value: any){
     switch(value){
          case true:
          case "true":
          case 1:
          case "1":
          case "on":
          case "yes":
              return true;
          default: 
              return false;
      }
  }

}