import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})
export class TicketService {
  constructor(private http: HttpClient) {}
  getMyTickets(): Observable<any> {
    
    return this.http.get(GlobalComponent.appUrl + 'ticket/tickets/');
  }
}
