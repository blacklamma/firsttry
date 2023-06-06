import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TicketService {
  constructor(private http: HttpClient) {}
  getMyTickets(): Observable<any> {
    
    return this.http.get('http://localhost:8000/ticket/tickets/');
  }
}
