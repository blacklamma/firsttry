import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NavbarComponent } from './navbar/navbar.component'
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TicketComponent } from './pages/ticket/ticket.component';
import { NgxPaginationModule } from 'ngx-pagination';
import { TicketService } from './pages/ticket/ticket.service';
import { TokenInterceptor } from './token.interceptor';
import { UserComponent } from './pages/user/user.component';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatButtonModule } from '@angular/material/button';
import { UseraddComponent } from './pages/user/useradd.component';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MyProfileComponent } from './pages/user/myprofile.component';
import { CustomerComponent } from './pages/customer/customer.component';
import { CustomerformComponent } from './pages/customer/customerform.component';
import { CustomerprofileComponent } from './pages/customer/customerprofile.component';
import { RolesComponent } from './pages/roles/roles.component';
import { RoleformComponent } from './pages/roles/roleform.component';
import { EmailComponent } from './pages/email/email.component';
import { WorkflowComponent } from './pages/workflow/workflow.component';
import { WorkflowformComponent } from './pages/workflow/workflowform.component';
import { NgSelectModule } from '@ng-select/ng-select'; 
import { MatTableModule } from '@angular/material/table';
import { NgxEditorModule } from 'ngx-editor';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    NavbarComponent,
    TicketComponent,
    UserComponent,
    UseraddComponent,
    MyProfileComponent,
    CustomerComponent,
    CustomerformComponent,
    CustomerprofileComponent,
    RolesComponent,
    RoleformComponent,
    EmailComponent,
    WorkflowComponent,
    WorkflowformComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    CommonModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    NgxPaginationModule,
    MatButtonModule, 
    MatTooltipModule,
    FormsModule,
    MatIconModule,
    MatSlideToggleModule,
    NgSelectModule,
    MatTableModule,
    NgxEditorModule
  ],
  providers: [
    AppComponent,
    TicketService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
