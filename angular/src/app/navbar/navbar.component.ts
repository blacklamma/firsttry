import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router'
import { FormGroup, FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  public logOutForm !: FormGroup;
  constructor(private formBuilder : FormBuilder, private http: HttpClient, private router: Router, private toastr: ToastrService){}
  ngOnInit(): void{
    this.logOutForm = this.formBuilder.group({
      username: [''],
      password: ['']
    })
  }
  logOut(){
    this.http.post('http://localhost:8000/user/logout/', {username: localStorage.getItem('username')}, {responseType: 'text'})
    .subscribe(
      (resData) => {
        console.log(resData)
        localStorage.setItem('username', '');
        this.toastr.success('Logged Out!', 'Success!');
        this.router.navigate(['']);
      }
    )
  }

}
