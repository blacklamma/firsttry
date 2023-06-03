import { ToastrService } from 'ngx-toastr';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router'
import conf_data from "./conf.json";

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
    this.http.post('http://localhost:8000/user/login/', this.loginForm.value, {responseType: 'text'})
    .subscribe(
      (resData) => {
        console.log(resData)
        localStorage.setItem('username', this.loginForm.value.username);
        this.loginForm.reset();
        this.toastr.success('Logged In!', 'Success!');
        this.router.navigate(['/home']);      
      }
    )
  }
}
