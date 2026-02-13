import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
@Injectable({
  providedIn: 'root',
})
export class Auth {
  private api = environment.apiUrl;

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {

  const body = new URLSearchParams();
  body.set('username', username);
  body.set('password', password);

  return this.http.post(
    `${this.api}/auth/login`,
    body.toString(),
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
    );
  }

  registerOwner(data: any) {
  return this.http.post(`${this.api}/auth/register-owner`, data);
}
  
  saveToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken() {
    return localStorage.getItem('token');
  }

  logout() {
    localStorage.removeItem('token');
  }
}
