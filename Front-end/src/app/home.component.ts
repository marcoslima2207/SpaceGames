import { ChangeDetectionStrategy, Component, OnDestroy, OnInit, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Game, GamesService } from './games.service';

@Component({
  selector: 'sg-home',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './home.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit, OnDestroy {
  private readonly gamesService = inject(GamesService);
  private readonly route = inject(ActivatedRoute);
  private rotation?: ReturnType<typeof setInterval>;
  readonly games = signal<Game[]>([]);
  readonly loading = signal(true);
  readonly error = signal(false);
  readonly query = signal('');
  readonly category = signal<number | 'all'>('all');
  readonly heroIndex = signal(0);
  readonly missionComplete = signal(localStorage.getItem('spacegames_mission') === 'complete');
  readonly featured = computed(() => this.games().filter((game) => game.destaque).slice(0, 5));
  readonly freeGames = computed(() => this.games().filter((game) => game.gratuito));
  readonly categories = computed(() => {
    const seen = new Map<number, string>();
    this.games().forEach((game) => { if (game.categoria && game.categoria_nome) seen.set(game.categoria, game.categoria_nome); });
    return Array.from(seen, ([id, name]) => ({ id, name }));
  });
  readonly filteredGames = computed(() => {
    const search = this.query().trim().toLocaleLowerCase();
    return this.games().filter((game) => {
      const matchesCategory = this.category() === 'all' || game.categoria === this.category();
      const searchable = `${game.titulo} ${game.descricao} ${game.desenvolvedor ?? ''}`.toLocaleLowerCase();
      return matchesCategory && (!search || searchable.includes(search));
    });
  });

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((params) => this.query.set(params.get('q') || ''));
    this.gamesService.getGames().subscribe({
      next: (games) => { this.games.set(games); this.loading.set(false); this.startRotation(); },
      error: () => { this.loading.set(false); this.error.set(true); }
    });
  }
  ngOnDestroy(): void { if (this.rotation) clearInterval(this.rotation); }
  selectCategory(category: number | 'all'): void { this.category.set(category); }
  nextHero(): void { const total = this.featured().length; if (total) this.heroIndex.update((index) => (index + 1) % total); }
  previousHero(): void { const total = this.featured().length; if (total) this.heroIndex.update((index) => (index - 1 + total) % total); }
  imageUrl(game: Game): string { return game.imagem_url_publica || game.imagem || '/media/jogos/space-default.jpg'; }
  onImageError(event: Event): void { (event.target as HTMLImageElement).src = 'https://placehold.co/900x560/10242d/e7f4ef?text=SPACEGAMES'; }
  formatPrice(game: Game): string { return game.gratuito ? 'Grátis' : Number(game.preco).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); }
  completeMission(): void {
    if (this.missionComplete()) return;
    this.missionComplete.set(true);
    const xp = Number(localStorage.getItem('spacegames_xp') || 740) + 120;
    localStorage.setItem('spacegames_mission', 'complete');
    localStorage.setItem('spacegames_xp', String(xp));
  }
  private startRotation(): void { if (this.featured().length > 1) this.rotation = setInterval(() => this.nextHero(), 6500); }
}