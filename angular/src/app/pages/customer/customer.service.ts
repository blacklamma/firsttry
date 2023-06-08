import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  constructor(private http: HttpClient) {}
  getCustomers(): Observable<any> {
    return this.http.get('http://localhost:8000/user/customers/');
  }
  getCustomer(id: string): Observable<any> {
    return this.http.get('http://localhost:8000/user/customers/' + id);
  }
  saveCustomer(data: any): Observable<any> {
    return this.http.post('http://localhost:8000/user/customers/', data);
  }
  deleteCustomer(id: string): Observable<any> {
    return this.http.delete('http://localhost:8000/user/customers/' + id);
  }
}
