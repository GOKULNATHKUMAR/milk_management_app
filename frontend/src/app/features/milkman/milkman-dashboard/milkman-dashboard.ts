import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-milkman-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './milkman-dashboard.html',
  styleUrl: './milkman-dashboard.css',
})
export class MilkmanDashboard {
constructor(private router: Router) {}

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}
