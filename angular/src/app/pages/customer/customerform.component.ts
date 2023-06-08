import { Component } from '@angular/core';
import { CustomerService } from './customer.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormGroup, FormBuilder, ReactiveFormsModule, FormControl, Validators } from '@angular/forms';
import { Location } from '@angular/common';
import { ConfirmPasswordValidator } from '../../confirm-password.validator';

@Component({
  selector: 'app-customerform',
  templateUrl: './customerform.component.html',
  styleUrls: ['./customer.component.css']
})
export class CustomerformComponent {
  
  id: any;
	avatarUrl: any;
  avatarMsg = "";
  event = 'add';
  public customerData !: FormGroup;
  constructor(private formBuilder : FormBuilder, private customerService: CustomerService, private route: ActivatedRoute, private toastr: ToastrService, private location: Location, private router: Router) {}

  ngOnInit(): void{
    this.id = this.route.snapshot.paramMap.get('id');
    this.customerData = this.formBuilder.group({
      id: [''],
      email: ['', Validators.required],
      customer_name: ['', Validators.required],
      avatarUrl: [''],
      password: [""],
      confirmPassword: [""],
      contact_number: [''],
      login_enabled: [false],
      username: [''],
      is_active: [false],
    },
    {
      validator: ConfirmPasswordValidator("password", "confirmPassword")
    });
    if(this.id){
      this.event = 'edit';
      this.customerService.getCustomer(this.id).subscribe(
        (response) => {
          this.customerData.setValue({
            id: response.id,
            email: response.email,
            customer_name: response.customer_name,
            avatarUrl: response.image_data,
            password: "*****************",
            confirmPassword: "*****************",
            contact_number: response.contact_number,
            login_enabled: response.login_enabled,
            is_active: response.is_active,
            username: response.username,
          });
          this.avatarUrl = response.image_data;
        }
      );
    }
  }

  saveCustomer(): void{ 
    this.customerService.saveCustomer(this.customerData.value).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('Customer data has been saved', 'Success!');
          this.router.navigate(['customer']);
        }
        else{
          this.toastr.error('Something went wrong :(', 'Error!');
        }
      }
    );
  }
  
  onAvatarSelected(event: any): void{
    const file:File = event.target.files[0];

    if (file){
      console.log(file);
      var mimeType = file.type;
      
      if (mimeType.match(/image\/*/) == null) {
        this.avatarMsg = "Only images are supported";
        return;
      }
      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (_event) => {
        this.avatarMsg = '';
        this.avatarUrl = reader.result; 
        console.log(this.avatarUrl)
        var fileData = {'name': file.name, 'data': this.avatarUrl, 'size': file.size, 'type': file.type, 'lastModified': file.lastModified};
        this.customerData.addControl('file', new FormControl(fileData));
        this.customerData.addControl('avatarUrl', new FormControl(this.avatarUrl));
      }
      console.log(file)
    }
    else{
			this.avatarMsg = 'You must select an image';
			return;
    }
  }

  goBack(): void{
    this.location.back();
  }

  public loginToggle(event: any) {
    this.customerData.patchValue({
      is_active: event.checked,
    });
  }
}
