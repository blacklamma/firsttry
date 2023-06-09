import { ToastrService } from 'ngx-toastr';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router'
import conf_data from "./conf.json";
import { GlobalComponent } from '../global-component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  public loginForm !: FormGroup;
  constructor(private formBuilder : FormBuilder, private http: HttpClient, private router: Router, private toastr: ToastrService){}
  ngOnInit(): void{

    this.loginForm = this.formBuilder.group({
      username: [''],
      password: ['']
    })
  }
  logIn(){
    this.http.post(GlobalComponent.appUrl + 'user/login/', this.loginForm.value)
    .subscribe(
      (resData: any) => {
        console.log(resData)
        localStorage.setItem('avatar', resData.profile_image);
        localStorage.setItem('userId', resData.user_id);
        localStorage.setItem('custId', resData.cust_id);
        localStorage.setItem('isStaff', resData.is_staff);
        localStorage.setItem('permissions', JSON.stringify(resData.permissions));
        
        this.http.post(GlobalComponent.appUrl + 'api/token/', this.loginForm.value)
        .subscribe(
          (data: any) => {
            localStorage.setItem('username', this.loginForm.value.username);
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('_authToken', data.access);
            this.loginForm.reset();
            this.toastr.success(resData.msg, 'Success!');
            this.router.navigate(['/home']);  
          })
      }
    )
  }
}
