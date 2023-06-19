import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})

export class EmailService {
  constructor(private http: HttpClient) {}

  // outgoing mails
  getOutEmails(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/emails/outEmails');
  }
  getOutConf(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/emails/getOutConf');
  }
  saveOutConf(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'wf/emails/saveOutConf/', data);
  }

  // incoming mails
  getInEmails(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/emails/inEmails');
  }
  getInConf(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/emails/getInConf');
  }
  saveInConf(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'wf/emails/saveInConf/', data);
  }
}
