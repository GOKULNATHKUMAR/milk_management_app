import { Component } from '@angular/core';
import { Auth } from '../../../core/auth';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule,RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  username = '';
  password = '';

  constructor(
    private auth: Auth,
    private router: Router
  ) {}

  login() {
  if (this.username.length !=10) {
      alert("Enter valid username");
      return;
    }
  this.auth.login(this.username, this.password)
    .subscribe({
  next:(res: any) => {
      this.auth.saveToken(res.access_token);
      localStorage.setItem('role', res.role);
    localStorage.setItem('user_id', res.user_id);

    if (res.role === 'owner') {
      this.router.navigate(['/owner']);
    } else if (res.role === 'milkman') {
      this.router.navigate(['/milkman']);
    }
  },
  error: () => {
    alert("Invalid Credentials");
  }
    });
}
}
