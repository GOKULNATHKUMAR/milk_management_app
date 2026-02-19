import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Milkman_data { 
  id: number; 
  name: string; 
  mobile: string; 
  language: string; 
  role: string; 
  owner_id: number; 
  is_active: boolean; 
  password?: string; 
}

@Injectable({
  providedIn: 'root',
})
export class Milkman {
  private api = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Add Milkman
  addMilkman(data: any): Observable<any> {
    return this.http.post(`${this.api}/auth/add-milkman`, data);
  }

  // Get Milkmen
  getMilkmen(): Observable<Milkman_data[]> {
    return this.http.get<Milkman_data[]>(`${this.api}/auth/milkmen`);
  }

  // Delete Milkman
  deleteMilkman(id: number): Observable<any> {
    return this.http.delete(`${this.api}/auth/milkman/${id}`);
  }
}
