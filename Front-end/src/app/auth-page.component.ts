import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

@Component({
  selector: 'sg-auth-page',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './auth-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AuthPageComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  readonly register = this.route.snapshot.data['mode'] === 'register';
  readonly submitted = signal(false);
  readonly error = signal('');
  username = '';
  email = '';
  name = '';
  password = '';
  confirmPassword = '';

  submit(): void {
    this.error.set('');
    const payload = this.register
      ? { username: this.username, email: this.email, password: this.password, first_name: this.name }
      : { username: this.username, password: this.password };
    const endpoint = this.register ? '/api/auth/register/' : '/api/token/';
    this.http.post<{ access: string; refresh: string }>(endpoint, payload).subscribe({
      next: (tokens) => {
        localStorage.setItem('spacegames_access', tokens.access);
        localStorage.setItem('spacegames_refresh', tokens.refresh);
        this.submitted.set(true);
        this.router.navigateByUrl('/');
      },
      error: (response: { error?: { detail?: string } | string }) => {
        const detail = typeof response.error === 'string' ? response.error : response.error?.detail;
        this.error.set(detail || 'Usuário ou senha inválidos.');
      }
    });
  }
}