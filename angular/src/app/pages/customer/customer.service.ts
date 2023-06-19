import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  constructor(private http: HttpClient) {}
  getCustomers(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'user/customers/');
  }
  getCustomer(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'user/customers/' + id);
  }
  saveCustomer(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'user/customers/', data);
  }
  deleteCustomer(id: string): Observable<any> {
    return this.http.delete(GlobalComponent.appUrl + 'user/customers/' + id);
  }
}
