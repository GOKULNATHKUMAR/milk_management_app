import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { Auth } from '../../../core/auth';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  name = '';
  mobile = '';
  password = '';
  confirmPassword = '';
  language = 'ta';
  is_milkman = false;   // if owner also collects milk

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
      language: this.language,
      is_milkman: this.is_milkman
    };

    this.authService.registerOwner(payload).subscribe({
      next: () => {
        alert("ROwner Registered Successfully");
        this.router.navigate(['/login']);
      },
      error: (err) => {
        alert(err.error?.detail || "Registration Failed");
      }
    });
  }
}
