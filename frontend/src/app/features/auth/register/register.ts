import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Auth } from '../../../core/auth';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  imports: [CommonModule, FormsModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  name = '';
  mobile = '';
  password = '';
  confirmPassword = '';
  role = 'owner';   // default
  language = 'ta';
  owner_id: number | null = null;

  constructor(
    private authService: Auth,
    private router: Router
  ) {}

  register() {

    if (this.password !== this.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    if (this.mobile.length !== 10) {
      alert("Enter valid 10 digit mobile number");
      return;
    }

    const payload = {
      name: this.name,
      mobile: this.mobile,
      password: this.password,
      role: this.role,
      language: this.language,
      owner_id: this.role === 'milkman' ? this.owner_id : null
    };

    this.authService.register(payload).subscribe({
      next: () => {
        alert("Registration Successful");
        this.router.navigate(['/login']);
      },
      error: (err) => {
        alert(err.error?.detail || "Registration Failed");
      }
    });
  }
}
