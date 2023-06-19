import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GlobalComponent } from '../../global-component';

@Injectable({
  providedIn: 'root'
})
export class WorkflowService {
  constructor(private http: HttpClient) {}
  getWorkflows(): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/wf/');
  }
  getWorkflow(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/wf/' + id);
  }
  getWorkflowOptions(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/wf/options/' + id);
  }
  saveWorkflow(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'wf/wf/', data);
  }
  deleteWorkflow(id: string): Observable<any> {
    return this.http.delete(GlobalComponent.appUrl + 'wf/wf/' + id);
  }
  saveStatus(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'wf/status/', data);
  }
  getStatuses(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/status/statusList/' + id);
  }
  saveRule(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'wf/rule/', data);
  }
  getRules(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/rule/rulesList/' + id);
  }
  saveNotif(data: any): Observable<any> {
    return this.http.post(GlobalComponent.appUrl + 'wf/notif/', data);
  }
  getNotifs(id: string): Observable<any> {
    return this.http.get(GlobalComponent.appUrl + 'wf/notif/notifList/' + id);
  }
}