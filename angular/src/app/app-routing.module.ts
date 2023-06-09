import { EmailComponent } from './pages/email/email.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './login/login.component';
import { TicketComponent } from './pages/ticket/ticket.component';
import { UserComponent } from './pages/user/user.component';
import { UseraddComponent } from './pages/user/useradd.component';
import { MyProfileComponent } from './pages/user/myprofile.component';
import { CustomerComponent } from './pages/customer/customer.component';
import { CustomerformComponent } from './pages/customer/customerform.component';
import { CustomerprofileComponent } from './pages/customer/customerprofile.component';
import { RolesComponent } from './pages/roles/roles.component';
import { RoleformComponent } from './pages/roles/roleform.component';
import { WorkflowComponent } from './pages/workflow/workflow.component';
import { WorkflowformComponent } from './pages/workflow/workflowform.component';

const routes: Routes = [
  { path: '', redirectTo:'login', pathMatch:'full'},
  { path: 'login', component: LoginComponent},
  { path: 'home', component: HomeComponent},

  // tickets
  { path: 'ticket', component: TicketComponent},
  
  // user
  { path: 'user', component: UserComponent},
  { path: 'user/add', component: UseraddComponent},
  { path: 'user/edit/:id', component: UseraddComponent},
  { path: 'myprofile', component: MyProfileComponent},

  // customer
  { path: 'customer', component: CustomerComponent},
  { path: 'customer/add', component: CustomerformComponent},
  { path: 'customer/edit/:id', component: CustomerformComponent},
  { path: 'custprofile', component: CustomerprofileComponent},

  // roles
  { path: 'roles', component: RolesComponent},
  { path: 'role/:id', component: RoleformComponent},

  // workflow
  { path: 'workflow', component: WorkflowComponent},
  { path: 'workflow/:event/:id', component: WorkflowformComponent},

  // email
  { path: 'email', component: EmailComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
