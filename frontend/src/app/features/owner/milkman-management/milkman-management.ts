import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Milkman, Milkman_data } from '../../../core/services/milkman';

@Component({
  selector: 'app-milkman-management',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './milkman-management.html',
  styleUrl: './milkman-management.css',
})
export class MilkmanManagement implements OnInit {
milkmen: Milkman_data[] = [];

  newMilkman = {
    name: '',
    mobile: '',
    password: '',
    language: 'en'
  };

  constructor(private milkmanService: Milkman) {}

  ngOnInit() {
    this.loadMilkmen();
  }
  
  loadMilkmen() {
    this.milkmanService.getMilkmen().subscribe({
      next: (res: Milkman_data[]) => {
        console.log("Backend response:", res); 
        this.milkmen = [...res];
      },
      error: (err) => console.error(err)
    });
  }

  
  addMilkman() {
    this.milkmanService.addMilkman(this.newMilkman).subscribe({
      next: () => {
        alert("Milkman Added");
        this.newMilkman = { name: '', mobile: '', password: '', language: 'en' };
        this.loadMilkmen();
      },
      error: (err) => alert(err.error.detail)
    });
  }

  deleteMilkman(id: number) {
    if (!confirm("Delete this milkman?")) return;

    this.milkmanService.deleteMilkman(id).subscribe({
      next: () => {
        alert("Deleted successfully");
        this.loadMilkmen();
      },
      error: (err) => console.error(err)
    });
  }
}
