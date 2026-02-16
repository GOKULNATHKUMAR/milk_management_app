import { CanActivateFn, Router} from '@angular/router';
import { inject } from '@angular/core';
export const roleGuard: CanActivateFn = (route, state) => {
  
  const router = inject(Router);
  const role = localStorage.getItem('role');
  const expectedRole = route.data?.['role'];

  if (role !== expectedRole) {
    router.navigate(['/login']);
    return false;
  }
  
  return true;
};
