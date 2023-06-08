
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}
  getUsers(): Observable<any> {
    return this.http.get('http://localhost:8000/user/users/');
  }
  getUser(id: string): Observable<any> {
    return this.http.get('http://localhost:8000/user/users/' + id);
  }
  getUserOptions(): Observable<any> {
    return this.http.get('http://localhost:8000/user/users/options');
  }
  saveUser(data: any): Observable<any> {
    return this.http.post('http://localhost:8000/user/users/', data);
  }
  deleteUser(id: string): Observable<any> {
    return this.http.delete('http://localhost:8000/user/users/' + id);
  }
}
