import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'sg-root',
  standalone: true,
  imports: [FormsModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent {
  query = '';
  private readonly router = inject(Router);
  readonly darkMode = signal(localStorage.getItem('spacegames_theme') !== 'light');
  readonly xp = signal(Number(localStorage.getItem('spacegames_xp') || 740));
  readonly level = computed(() => Math.floor(this.xp() / 1000) + 1);
  readonly levelProgress = computed(() => this.xp() % 1000);
  readonly missionComplete = signal(localStorage.getItem('spacegames_mission') === 'complete');

  search(): void {
    this.router.navigate(['/'], { queryParams: { q: this.query } });
  }

  toggleTheme(): void {
    this.darkMode.update((dark) => !dark);
    localStorage.setItem('spacegames_theme', this.darkMode() ? 'dark' : 'light');
  }

  isLoggedIn(): boolean {
    return Boolean(localStorage.getItem('spacegames_access'));
  }

  logout(): void {
    localStorage.removeItem('spacegames_access');
    localStorage.removeItem('spacegames_refresh');
    this.router.navigateByUrl('/login');
  }

  completeMission(): void {
    if (this.missionComplete()) return;
    this.missionComplete.set(true);
    this.xp.update((value) => value + 120);
    localStorage.setItem('spacegames_mission', 'complete');
    localStorage.setItem('spacegames_xp', String(this.xp()));
  }
}