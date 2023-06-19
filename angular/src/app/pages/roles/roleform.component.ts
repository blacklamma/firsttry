
import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Location } from '@angular/common';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})
@Component({
  selector: 'app-roles',
  templateUrl: './roleform.component.html',
  styleUrls: ['./roles.component.css']
})
export class RoleformComponent implements OnInit {

  id: any;
  role : any ={'name': ''};
  permissions : any[] = [];
  updatedRoles: any = {};
  constructor(private route: ActivatedRoute, private toastr: ToastrService, 
    private location: Location, private router: Router, private http: HttpClient) {}

  ngOnInit(): void{
    this.id = this.route.snapshot.paramMap.get('id');
    this.http.get(GlobalComponent.appUrl + 'user/role/' + this.id).subscribe(
      (response: any) => {
        this.role = response;
        let permModules = Object.keys(this.role.permission);
        let i = 0;
        for (let perm of permModules){
          this.permissions.push({});
          this.permissions[i]['name'] = perm;
          let perms = this.role.permission[perm];
          let permKeys = Object.keys(perms);
          let j = 0;
          let permList : any[] = [];
          for (let key of permKeys){
            permList.push({'name': key, 'value': perms[key]});
            j++;
          }
          this.permissions[i]['perms'] = permList;
          i++;
        }
      }
    );
  }
  public updateInfo(key: string, module: string, event: MatSlideToggleChange): void{
    this.updatedRoles[key + '_' + module] = event.source.checked;
  }
  public saveRole(): void{
    let params = {'updated_roles': this.updatedRoles, 'role': this.role.id};
    this.http.post(GlobalComponent.appUrl + 'user/role/', params).subscribe(
      (response: any) => {
        if(response.status == 'success'){
          this.toastr.success('Role Permissions have been saved', 'Success!');
          this.router.navigate(['roles']);
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
  goBack(): void{
    this.location.back();
  }
}
