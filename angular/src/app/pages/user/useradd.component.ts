import { Component } from '@angular/core';
import { UserService } from './user.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormGroup, FormBuilder, ReactiveFormsModule, FormControl, Validators } from '@angular/forms';
import { Location } from '@angular/common';
import { ConfirmPasswordValidator } from '../../confirm-password.validator';

@Component({
  selector: 'app-useradd',
  templateUrl: './useradd.component.html',
  styleUrls: ['./user.component.css']
})
export class UseraddComponent {
  
  id: any;
	avatarUrl: any;
  avatarMsg = "";
  public userData !: FormGroup;
  constructor(private formBuilder : FormBuilder, private userService: UserService, private route: ActivatedRoute, private toastr: ToastrService, private location: Location, private router: Router) {}

  ngOnInit(): void{
    this.id = this.route.snapshot.paramMap.get('id');
    this.userData = this.formBuilder.group({
      id: [''],
      username: ['', Validators.required],
      email: ['', Validators.required],
      first_name: ['', Validators.required],
      last_name: [''],
      is_active: [false],
      avatarUrl: [''],
      password: ["", Validators.required],
      confirmPassword: ["", Validators.required],
      department: [''],
      designation: [''],
      contact_number: ['']
    },
    {
      validator: ConfirmPasswordValidator("password", "confirmPassword")
    });
    if(this.id){
      this.userService.getUser(this.id).subscribe(
        (response) => {
          this.userData.setValue({
            id: response.id,
            username: response.username,
            email: response.email,
            first_name: response.first_name,
            last_name: response.last_name,
            is_active: response.is_active,
            avatarUrl: response.profile.image_data,
            password: "*****************",
            confirmPassword: "*****************",
            department: response.profile.department,
            designation: response.profile.designation,
            contact_number: response.profile.contact_number,
          });
          this.avatarUrl = response.profile.image_data;
        }
      );
    }
    else{
    }
  }

  saveUser(): void{ 
    this.userService.saveUser(this.userData.value).subscribe(
      (response) => {
        if(response.status == 'success'){
          this.toastr.success('User data has been saved', 'Success!');
          if(this.userData.value.avatarUrl){
            localStorage.setItem('avatar', this.userData.value.avatarUrl);
          }
          this.router.navigate(['user']);
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
        this.userData.addControl('file', new FormControl(fileData));
        this.userData.addControl('avatarUrl', new FormControl(this.avatarUrl));
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
}
