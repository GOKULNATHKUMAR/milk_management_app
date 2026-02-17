import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-milkman-management',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './milkman-management.html',
  styleUrl: './milkman-management.css',
})
export class MilkmanManagement {

}
