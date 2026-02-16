import { Routes } from '@angular/router';
import { roleGuard } from './core/role-guard';
import { authGuard } from './core/auth-guard';

export const routes: Routes = [
    {
  path: '',
  loadComponent: () =>
    import('./home/home').then(m => m.Home)
},
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/login/login')
        .then(m => m.Login)
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./features/auth/register/register')
        .then(m => m.Register)
  },
  {
  path: 'owner',
  canActivate: [authGuard, roleGuard],
  data: { role: 'owner' },
  loadComponent: () =>
    import('./features/owner/owner-dashboard/owner-dashboard')
      .then(m => m.OwnerDashboard)
},

{
  path: 'milkman',
  canActivate: [authGuard, roleGuard],
  data: { role: 'milkman' },
  loadComponent: () =>
    import('./features/milkman/milkman-dashboard/milkman-dashboard')
      .then(m => m.MilkmanDashboard)
},
];
