
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}
  getUsers(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'user/users/');
  }
  getUser(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'user/users/' + id);
  }
  getUserOptions(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'user/users/options');
  }
  saveUser(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'user/users/', data);
  }
  deleteUser(id: string): Observable<any> {
    return this.http.delete(GlobalComponent.appUrl + 'user/users/' + id);
  }
}
