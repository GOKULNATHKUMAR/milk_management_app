import { Routes } from '@angular/router';
import { roleGuard } from './core/role-guard';
import { authGuard } from './core/auth-guard';
import { OwnerDashboard } from './features/owner/owner-dashboard/owner-dashboard';
import { MilkmanDashboard } from './features/milkman/milkman-dashboard/milkman-dashboard';

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
{
  path: 'owner',
  component: OwnerDashboard,
  children: [
    {
      path: 'milkman',
      loadComponent: () =>
        import('./features/owner/milkman-management/milkman-management')
          .then(m => m.MilkmanManagement)
    },
    {
      path: 'intake',
      loadChildren: () =>
        import('./features/intake/intake-module')
          .then(m => m.IntakeModule)
    },
    {
      path: 'sales',
      loadChildren: () =>
        import('./features/sales/sales-module')
          .then(m => m.SalesModule)
    },
    {
      path: 'reports',
      loadChildren: () =>
        import('./features/reports/reports-module')
          .then(m => m.ReportsModule)
    },
    {
      path: 'whatsapp',
      loadChildren: () =>
        import('./features/reports/reports-module')
          .then(m => m.ReportsModule)
    }
  ]
},
{
  path: 'milkman',
  component: MilkmanDashboard,
  children: [
    {
      path: 'intake',
      loadChildren: () =>
        import('./features/intake/intake-module')
          .then(m => m.IntakeModule)
    },
    {
      path: 'sales',
      loadChildren: () =>
        import('./features/sales/sales-module')
          .then(m => m.SalesModule)
    }
  ]
},
];
