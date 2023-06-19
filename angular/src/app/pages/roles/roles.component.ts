import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})
@Component({
  selector: 'app-roles',
  templateUrl: './roles.component.html',
  styleUrls: ['./roles.component.css']
})
export class RolesComponent implements OnInit  {

  roles : any;
  constructor(private http: HttpClient, private router: Router) {}
  ngOnInit(): void{
    this.http.get(GlobalComponent.appUrl + 'user/role/').subscribe(
      (response: any) => {
        this.roles = response;
      }
    );
  }
  
  public openRoleEdit(roleId: any): void{
    this.router.navigate(['role/' + roleId]);
  }
}
