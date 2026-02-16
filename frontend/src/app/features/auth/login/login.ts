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
    .subscribe((res: any) => {
      this.auth.saveToken(res.access_token);
      alert('Login successful');
      this.router.navigate(['/']);
    });
}
}
